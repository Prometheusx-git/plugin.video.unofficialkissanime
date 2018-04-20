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


from resources.lib.common.helpers import helper
from resources.lib.common.args import args
from dat1guy.shared.lastshowvisited import LastShowVisited


class LastVisited(LastShowVisited):
    def __init__(self):
        LastShowVisited.__init__(self, helper.get_profile())

    def update_last_show_visited(self):
        tmp_args = args.__dict__
        LastShowVisited.update_last_show_visited(self, tmp_args)

    def _create_table(self):
        LastShowVisited._create_table(self)

        # The move to using the dat1guy.shared module introduced a change in
        # schema, so we perform a one-time update to the schema below
        sql_select = 'PRAGMA table_info(last_visited)'
        self.dbcur.execute(sql_select)
        rows = self.dbcur.fetchall()
        columns = [row['name'] for row in rows]
        if 'full_mc_name' in columns:
            helper.log_notice('Updating last_visited table schema')
            sql_alter1 = 'ALTER TABLE last_visited RENAME TO last_visited_old'
            sql_alter2 = 'CREATE TABLE last_visited ('\
                'id TEXT, action TEXT, value TEXT, icon TEXT, '\
                'fanart TEXT, full_title TEXT, base_title TEXT, '\
                'imdb_id TEXT, tvdb_id TEXT, tmdb_id TEXT, '\
                'media_type TEXT, UNIQUE(id))'
            sql_alter3 = 'INSERT INTO last_visited('\
                'id, action, value, icon, fanart, full_title, base_title, '\
                'imdb_id, tvdb_id, tmdb_id, media_type) '\
                'SELECT id, action, value, icon, fanart, full_mc_name, '\
                'base_mc_name, imdb_id, tvdb_id, tmdb_id, media_type '\
                'FROM last_visited_old'
            sql_alter4 = 'DROP TABLE last_visited_old'
            self.dbcur.execute(sql_alter1)
            self.dbcur.execute(sql_alter2)
            self.dbcur.execute(sql_alter3)
            self.dbcur.execute(sql_alter4)