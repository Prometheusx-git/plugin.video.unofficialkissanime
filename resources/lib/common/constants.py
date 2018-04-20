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


plugin_name = 'plugin.video.unofficialkissanime'
domain = 'kissanime.ru'
runplugin = 'XBMC.RunPlugin(%s)'
appdata_cache_path = 'appdata.db'


submenu_browse = [
    ('A-Z', {'value':'submenu_alphabet', 'action':'localList'}),
    ('Popular', {'value':'/AnimeList/MostPopular', 'action':'mediaContainerList'}),
    ('Last updated', {'value':'/AnimeList/LatestUpdate', 'action':'mediaContainerList'}),
    ('Newest', {'value':'/AnimeList/Newest', 'action':'mediaContainerList'}),
    ('Upcoming', {'value':'UpcomingAnime', 'action':'mediaContainerList'}),
    ('Genre', {'value':'submenu_genres', 'action':'localList'}),
    ('Ongoing', {'value':'Status/Ongoing/MostPopular', 'action':'mediaContainerList'}),
    ('Completed', {'value':'Status/Ongoing/MostPopular', 'action':'mediaContainerList'})
]

submenu_alphabet = [
    ('All', {'value':'/AnimeList', 'action':'mediaContainerList'}),
    ('#', {'value':'/AnimeList?c=0', 'action':'mediaContainerList'}),
    ('A', {'value':'/AnimeList?c=a', 'action':'mediaContainerList'}),
    ('B', {'value':'/AnimeList?c=b', 'action':'mediaContainerList'}),
    ('C', {'value':'/AnimeList?c=c', 'action':'mediaContainerList'}),
    ('D', {'value':'/AnimeList?c=d', 'action':'mediaContainerList'}),
    ('E', {'value':'/AnimeList?c=e', 'action':'mediaContainerList'}),
    ('F', {'value':'/AnimeList?c=f', 'action':'mediaContainerList'}),
    ('G', {'value':'/AnimeList?c=g', 'action':'mediaContainerList'}),
    ('H', {'value':'/AnimeList?c=h', 'action':'mediaContainerList'}),
    ('I', {'value':'/AnimeList?c=i', 'action':'mediaContainerList'}),
    ('J', {'value':'/AnimeList?c=j', 'action':'mediaContainerList'}),
    ('K', {'value':'/AnimeList?c=k', 'action':'mediaContainerList'}),
    ('L', {'value':'/AnimeList?c=l', 'action':'mediaContainerList'}),
    ('M', {'value':'/AnimeList?c=m', 'action':'mediaContainerList'}),
    ('N', {'value':'/AnimeList?c=n', 'action':'mediaContainerList'}),
    ('O', {'value':'/AnimeList?c=o', 'action':'mediaContainerList'}),
    ('P', {'value':'/AnimeList?c=p', 'action':'mediaContainerList'}),
    ('Q', {'value':'/AnimeList?c=q', 'action':'mediaContainerList'}),
    ('R', {'value':'/AnimeList?c=r', 'action':'mediaContainerList'}),
    ('S', {'value':'/AnimeList?c=s', 'action':'mediaContainerList'}),
    ('T', {'value':'/AnimeList?c=t', 'action':'mediaContainerList'}),
    ('U', {'value':'/AnimeList?c=u', 'action':'mediaContainerList'}),
    ('V', {'value':'/AnimeList?c=v', 'action':'mediaContainerList'}),
    ('W', {'value':'/AnimeList?c=w', 'action':'mediaContainerList'}),
    ('X', {'value':'/AnimeList?c=x', 'action':'mediaContainerList'}),
    ('Y', {'value':'/AnimeList?c=y', 'action':'mediaContainerList'}),
    ('Z', {'value':'/AnimeList?c=z', 'action':'mediaContainerList'})
]

submenu_genres = [
    ('Action', {'value':'Genre/Action/MostPopular', 'action':'mediaContainerList'}),
    ('Adventure', {'value':'Genre/Adventure/MostPopular', 'action':'mediaContainerList'}),
    ('Cars', {'value':'Genre/Cars/MostPopular', 'action':'mediaContainerList'}),
    ('Cartoon', {'value':'Genre/Cartoon/MostPopular', 'action':'mediaContainerList'}),
    ('Comedy', {'value':'Genre/Comedy/MostPopular', 'action':'mediaContainerList'}),
    ('Dementia', {'value':'Genre/Dementia/MostPopular', 'action':'mediaContainerList'}),
    ('Demons', {'value':'Genre/Demons/MostPopular', 'action':'mediaContainerList'}),
    ('Drama', {'value':'Genre/Drama/MostPopular', 'action':'mediaContainerList'}),
    ('Dub', {'value':'Genre/Dub/MostPopular', 'action':'mediaContainerList'}),
    ('Ecchi', {'value':'Genre/Ecchi/MostPopular', 'action':'mediaContainerList'}),
    ('Fantasy', {'value':'Genre/Fantasy/MostPopular', 'action':'mediaContainerList'}),
    ('Game', {'value':'Genre/Game/MostPopular', 'action':'mediaContainerList'}),
    ('Harem', {'value':'Genre/Harem/MostPopular', 'action':'mediaContainerList'}),
    ('Historical', {'value':'Genre/Historical/MostPopular', 'action':'mediaContainerList'}),
    ('Horror', {'value':'Genre/Horror/MostPopular', 'action':'mediaContainerList'}),
    ('Josei', {'value':'Genre/Josei/MostPopular', 'action':'mediaContainerList'}),
    ('Kids', {'value':'Genre/Kids/MostPopular', 'action':'mediaContainerList'}),
    ('Magic', {'value':'Genre/Magic/MostPopular', 'action':'mediaContainerList'}),
    ('Martial Arts', {'value':'Genre/Martial-Arts/MostPopular', 'action':'mediaContainerList'}),
    ('Mecha', {'value':'Genre/Mecha/MostPopular', 'action':'mediaContainerList'}),
    ('Military', {'value':'Genre/Military/MostPopular', 'action':'mediaContainerList'}),
    ('Movie', {'value':'Genre/Movie/MostPopular', 'action':'mediaContainerList'}),
    ('Music', {'value':'Genre/Music/MostPopular', 'action':'mediaContainerList'}),
    ('Mystery', {'value':'Genre/Mystery/MostPopular', 'action':'mediaContainerList'}),
    ('ONA', {'value':'Genre/ONA/MostPopular', 'action':'mediaContainerList'}),
    ('OVA', {'value':'Genre/OVA/MostPopular', 'action':'mediaContainerList'}),
    ('Parody', {'value':'Genre/Parody/MostPopular', 'action':'mediaContainerList'}),
    ('Police', {'value':'Genre/Police/MostPopular', 'action':'mediaContainerList'}),
    ('Psychological', {'value':'Genre/Psychological/MostPopular', 'action':'mediaContainerList'}),
    ('Romance', {'value':'Genre/Romance/MostPopular', 'action':'mediaContainerList'}),
    ('Samurai', {'value':'Genre/Samurai/MostPopular', 'action':'mediaContainerList'}),
    ('School', {'value':'Genre/School/MostPopular', 'action':'mediaContainerList'}),
    ('Sci-Fi', {'value':'Genre/Sci-Fi/MostPopular', 'action':'mediaContainerList'}),
    ('Seinen', {'value':'Genre/Seinen/MostPopular', 'action':'mediaContainerList'}),
    ('Shoujo', {'value':'Genre/Shoujo/MostPopular', 'action':'mediaContainerList'}),
    ('Shoujo Ai', {'value':'Genre/Shoujo-Ai/MostPopular', 'action':'mediaContainerList'}),
    ('Shounen', {'value':'Genre/Shounen/MostPopular', 'action':'mediaContainerList'}),
    ('Shounen Ai', {'value':'Genre/Shounen-Ai/MostPopular', 'action':'mediaContainerList'}),
    ('Slice of Life', {'value':'Genre/Slice-of-Life/MostPopular', 'action':'mediaContainerList'}),
    ('Space', {'value':'Genre/Space/MostPopular', 'action':'mediaContainerList'}),
    ('Special', {'value':'Genre/Special/MostPopular', 'action':'mediaContainerList'}),
    ('Sports', {'value':'Genre/Sports/MostPopular', 'action':'mediaContainerList'}),
    ('Super Power', {'value':'Genre/Super-Power/MostPopular', 'action':'mediaContainerList'}),
    ('Supernatural', {'value':'Genre/Supernatural/MostPopular', 'action':'mediaContainerList'}),
    ('Thriller', {'value':'Genre/Thriller/MostPopular', 'action':'mediaContainerList'}),
    ('Vampire', {'value':'Genre/Vampire/MostPopular', 'action':'mediaContainerList'}),
    ('Yuri', {'value':'Genre/Yuri/MostPopular', 'action':'mediaContainerList'})
]

main_menu = [
    ('Last Anime Visited', {'value':'sql', 'action':'lastvisited'}),
    ('Browse', {'value':'submenu_browse', 'action':'localList'}),
    ('Bookmarks', {'value':'/BookmarkList', 'action':'bookmarkList'}),
    ('Search', {'value':'dialog_search', 'action':'search'}),
    ('Settings', {'value':'settings', 'action':'settings'})
]

ui_table = {
    'main_menu' : main_menu,
    'submenu_browse' : submenu_browse,
    'submenu_alphabet' : submenu_alphabet,
    'submenu_genres' : submenu_genres
}