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


import re
from resources.lib.common.args import args
from resources.lib.common.helpers import helper
from resources.lib.common.webpage import WebPage
from bs4 import BeautifulSoup


class WebList(WebPage):
    def __init__(self, url_val=args.value, form_data=None):       
        WebPage.__init__(self, url_val, form_data)
        self.links = []
        self.has_next_page = False
        from resources.lib.metadata.metadatahandler import meta
        self.meta = meta

    def parse(self):
        pass

    def add_items(self):
        pass

    def get_metadata(self):
        pass

    def clean_name(self, name, specials=True):
        cleaned_name = name.replace(' (Sub)', '').replace(' (Dub)', '')
        if specials:
            cleaned_name = cleaned_name.replace(' (OVA)', '').replace(' Specials ', '')
            cleaned_name = self._strip_by_re(cleaned_name, '( OVA)$', end=-4)
            cleaned_name = self._strip_by_re(cleaned_name, '( Special)$', end=-8)
            cleaned_name = self._strip_by_re(cleaned_name, '( Specials)$', end=-9)
        cleaned_name = self._strip_by_re(cleaned_name, '( \(1080p\))$', end=-8)
        cleaned_name = self._strip_by_re(cleaned_name, '( \((720|480|360)p\))$', end=-8)
        return cleaned_name

    def _get_art_from_metadata(self, metadata):
        icon = metadata.get('cover_url', args.icon)
        fanart = metadata.get('backdrop_url', args.fanart)
        return (icon, fanart)

    def _construct_query(self, value, action, metadata={}, full_title='', media_type=''):
        icon, fanart = self._get_art_from_metadata(metadata)
        base_title = metadata.get('title', '')
        imdb_id = metadata.get('imdb_id', '')
        tvdb_id = metadata.get('tvdb_id', '')
        tmdb_id = metadata.get('tmdb_id', '')
        query = {'value':value, 'action':action, 'imdb_id':imdb_id, 
                 'tvdb_id':tvdb_id, 'tmdb_id':tmdb_id, 'icon':icon, 'fanart':fanart,
                 'base_title':base_title, 'full_title':full_title, 'media_type':media_type}
        return query
    
    # This may belong somewhere else...
    def _strip_by_re(self, string, filter, end, start=0):
        return string[start:end] if re.search(filter, string) != None else string


