# -*- coding: utf-8 -*-
'''
    The Unofficial KissAnime Plugin, aka UKAP - a plugin for Kodi
    Copyright (C) 2016 dat1guy

    This file is part of UKAP.

    UKAP is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    UKAP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with UKAP.  If not, see <http://www.gnu.org/licenses/>.
'''


import re, unicodedata
from datetime import datetime
from resources.lib.common import constants
from resources.lib.common.args import args
from resources.lib.common.helpers import helper
from resources.lib.list_types.web_list import WebList
from resources.lib.list_types import media_container_list
from bs4 import BeautifulSoup


class EpisodeList(WebList):
    def __init__(self):
        WebList.__init__(self)
        self.genres = []
        self.aliases = []
        self.related_links = []
        self.first_air_date = ''
        self.season = None
        self.num_episodes = 0

    ''' PUBLIC FUNCTIONS '''
    def parse(self):
        helper.start('EpisodeList.parse')
        if self.soup == None:
            return

        # Note that there are some lists/listings that do not have any episodes (!)
        table = self.soup.find('table', class_='listing')
        self.links = table.find_all('a') if table else []
        spans = self.soup.find_all('span', class_='info')
        helper.log_debug('# of links found: %d' % len(self.links))

        # We can determine if the media is a movie or not examining the genres
        span = [s for s in spans if s.string == 'Genres:']
        if span != []:
            genre_links = span[0].parent.find_all('a')
            self.genres = [link.string for link in genre_links]
            helper.log_debug('Found the genres: %s' % str(self.genres))

        # We'll try to determine the episode list from the first date
        span = [s for s in spans if s.string == 'Date aired:']
        if span != []:
            air_date = span[0].next_sibling.encode('ascii', 'ignore').strip().split(' to ')[0]
            air_datetime = helper.get_datetime(air_date, '%b %d, %Y')
            self.first_air_date = air_datetime.strftime('%Y-%m-%d')
            helper.log_debug('Found the first air date: %s' % str(self.first_air_date))

        # We'll try to determine the season from the alternate names, if necessary
        span = [s for s in spans if s.string == 'Other name:']
        if span != []:
            alias_links = span[0].parent.find_all('a')
            # Only keep aliases that do not contain CJK (eg, Japanese) characters
            f = lambda c: ord(c) > 0x3000
            self.aliases = [link.string for link in alias_links if filter(f, link.string) == u'']
            helper.log_debug('Found the aliases: %s' % str(self.aliases))

        # Grab the related links and the bookmark ID
        rightboxes = self.soup.find('div', id='rightside').find_all('div', class_='rightBox')
        if len(rightboxes) > 1:
            related = rightboxes[1].find('div', class_='barContent').find_all('a')
            for link in related:
                self.related_links.append(link)
                # Sometimes the related container includes episodes which are 
                # dead links.  This is the best way to filter them out.
                try:
                    has_class = dict(link.next_sibling.next_sibling.attrs).has_key('class')
                    if has_class and link.next_sibling.next_sibling['class'][0] == u'line':
                        break
                except:
                    pass

        self.bookmark_id = self.html.split('animeID=')[1].split('"')[0] if 'animeID=' in self.html else None

        # Sort episodes in ascending order by default
        self.links.reverse()

        helper.end('EpisodeList.parse')
        return
    
    def get_actual_media_type(self):
        # 1.1) The metadata classification may have failed earlier before because
        # of lack of data.  We can fix any potential mismatches here.
        if 'Movie' in self.genres:
            helper.log_debug('|COUNT|MISMATCH| %s' % args.full_title)
            return 'tvshow'#'movie'

        # 1.2) We have a special, let's handle just use the season 0 data along with the show banner
        if 'OVA' in self.genres or ('(OVA)' in args.full_title or ' Specials' in args.full_title or
            re.search('( OVA)( \(((Sub)|(Dub))\))?$', args.full_title) != None or
            re.search(' (Special)$', args.full_title) != None):
            helper.log_debug('|COUNT|OVA| %s' % args.full_title)
            return 'tvshow'#'special'

        return 'tvshow'

    def add_items(self):
        helper.start('EpisodeList.add_items')
        if self.links == []:
            return

        # We now have a list of episodes in links, and we need to figure out
        # which season those episodes belong to, as well as filter out stray
        # specials/OVAs.  I have a numbered FSM for this.  The caller should
        # invoke get_actual_media_type before this function to get the first state.
        
        # 2) Otherwise, we have a tv show.  The most reliable way to figure out 
        # what data to use is to use the first air date with the number of 
        # episodes.
        self.season = None
        if self.first_air_date == '':
            # 3) If we don't have the air date, we will try our best to 
            # determine which season this is based on the data we scraped
            self.season = self.__determine_season()
            if self.season == None:
                # I'm not sure what the next best step is here, but I have to
                # assume it's the first season to catch a lot of actual first 
                # seasons...
                helper.log_debug('|COUNT|LEFTOVER| %s' % args.full_title)
        else:
            helper.log_debug('|COUNT|AIR| %s' % args.full_title)

        specials = []
        episodes = []
        double_eps, half_eps = 0, 0
        for link in self.links:
            name = link.string.strip()
            url = link['href']
            if isinstance(name, unicode):
                ascii_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            else:
                ascii_name = name
            name_minus_show = ascii_name.replace(args.full_title, '')
            if self.__is_episode_special(name, name_minus_show):
                specials.append((name, url))
            else:
                if self.__is_double_episode(name):
                    double_eps += 1
                elif self.__is_half_episode(name):
                    half_eps += 1
                episodes.append((name, url))

        self.num_episodes = len(episodes) + double_eps - half_eps
        helper.log_debug('We have effectively %d episodes with %s double episodes and %d half episodes' % (self.num_episodes, double_eps, half_eps))

        all_metadata = self.get_metadata(args.base_title)
        helper.log_debug('We have %d metadata entries' % len(all_metadata))
        offset = 0
        for idx, (name, url) in enumerate(episodes):
            if self.__is_half_episode(name):
                offset -= 1
            metadata = all_metadata[idx+offset] if idx+offset < len(all_metadata) else {'title':name}
            icon, fanart = self._get_art_from_metadata(metadata)
            query = self._construct_query(url, 'qualityPlayer', metadata)
            if self.__is_double_episode(name):
                metadata['title'] = '%d & %d - %s' % ((idx+offset+1), (idx+offset+2), metadata['title'])
                offset += 1
            else:
                metadata['title'] = '%d - %s' % ((idx+offset+1), metadata['title'])
            contextmenu_items = self._get_contextmenu_items(url, name)
            helper.add_video_item(query, metadata, img=icon, fanart=fanart, contextmenu_items=contextmenu_items)

        if len(specials) > 0:
            icon, fanart = self._get_art_for_season0()
            for (name, url) in specials:
                metadata = {'title':name}
                query = self._construct_query(url, 'qualityPlayer', metadata)
                helper.add_video_item(query, metadata, img=icon, fanart=fanart)

        self._add_related_links()
        self._add_bookmark_link()

        helper.set_content('episodes')
        helper.add_sort_methods(['title'])
        helper.end_of_directory()
        helper.end('EpisodeList.add_items')
        return

    def get_metadata(self, name):
        if (helper.get_setting('enable-metadata') == 'false' or 
            (args.imdb_id == None and args.tvdb_id == None)):
            return []
        
        all_metadata = self.meta.get_episodes_meta(name, args.imdb_id, args.tvdb_id, self.num_episodes,
                                                   self.first_air_date, self.season)

        return all_metadata

    ''' PROTECTED FUNCTIONS '''
    def _get_contextmenu_items(self, url, name):
        contextmenu_items = [('Show information', 'XBMC.Action(Info)'), ('Queue item', 'XBMC.Action(Queue)')]
        show_queue_query = self._construct_query('', 'showqueue')
        show_queue_context_item = constants.runplugin % helper.build_plugin_url(show_queue_query)
        contextmenu_items.append(('Show queue', show_queue_context_item))
        return contextmenu_items

    def _get_art_for_season0(self):
        helper.start('_get_art_for_season0 for name %s and imdb_id %s' % (args.base_title, args.imdb_id))
        if helper.get_setting('enable-metadata') == 'false':
            return None, ''

        season_covers = self.meta.get_seasons(args.base_title, args.imdb_id, ['0'])
        if len(season_covers) > 0:
            icon = season_covers[0]['cover_url']
            fanart = season_covers[0]['backdrop_url']
        else:
            icon = args.icon
            fanart = args.fanart
        return icon, fanart

    def _add_related_links(self):
        # Add related links using the MCL (since they're all media containers)
        if len(self.related_links) > 0:
            mclist = media_container_list.MediaContainerList(None)
            mclist.links = self.related_links
            mclist.add_items(title_prefix='Related: ')

    def _add_bookmark_link(self):
        if self.bookmark_id != None:
            query = self._construct_query(self.bookmark_id, 'toggleBookmark')
            helper.add_directory(query, {'title':'Toggle bookmark'})

    ''' PRIVATE FUNCTIONS '''
    def __determine_season(self):
        # 3.1) The next best thing is to examine the full name vs the base 
        # name and look for any season stuff
        clean_title = self.clean_name(args.full_title)
        leftovers = clean_title.replace(args.base_title, '')
        season = self.__extract_season(leftovers)
        if season != None:
            helper.log_debug('|COUNT|BASE| %s' % args.full_title)
            # We have a season, let's extract it and work from there
            return season

        # 3.2) The next best thing after that is to examine the alternate 
        # names and look for any season stuff
        for alias in self.aliases:
            season = self.__extract_season(alias)
            if season != None:
                helper.log_debug('|COUNT|ALIAS| %s' % args.full_title)
                return season

        return None

    def __extract_season(self, name):
        season = None
        name = name.replace(' (TV)', '')
        if ' Second Season' in name or ' 2nd Season' in name:
            season = str(2)
        elif re.search('( Season [0-9])$', name) != None:
            season = name[-1]
        elif re.search('( S[0-9])$', name) != None:
            season = name[-1]
        elif re.search('( II)$', name) != None:
            season = str(2)
        elif re.search('( [0-9])$', name):
            season = name[-1]
        return season

    def __is_episode_special(self, name, name_minus_show):
        is_special = re.search('( .?Special ([0-9]?){0,2}[0-9])$', name) != None or \
            'recap' in name_minus_show.lower() or \
            '.5' in name_minus_show or \
            'preview' in name_minus_show.lower() or \
            re.search('( _Episode [0-9]{1,3})', name) != None or \
            re.search('( _Opening)', name) != None or \
            re.search('( _Ending)', name) != None
        return is_special

    def __is_double_episode(self, name):
        is_double = re.search('( Episode [0-9]{1,3}-[0-9]{0,3})$', name) != None
        return is_double

    def __is_half_episode(self, name):
        is_half = re.search('( Episode [0-9]{1,3}[Bb])$', name) != None
        return is_half