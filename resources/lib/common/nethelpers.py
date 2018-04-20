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


import os, xbmcvfs
from dat1guy.shared.nethelper import NetHelper
from resources.lib.common.helpers import helper


def __init():
    cookies = helper.get_profile() + 'cookies.txt'
    net = NetHelper(cookies, True)

    # Make sure the cookies exist
    if not os.path.exists(cookies):
        cookiesfile = xbmcvfs.File(cookies, 'w')
        cookiesfile.close()

    return cookies, net


cookies, net = __init()