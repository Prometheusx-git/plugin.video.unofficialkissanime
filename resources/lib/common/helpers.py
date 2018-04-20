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


import sys
from dat1guy.shared import helper as shared_helper
from resources.lib.common import constants


# I like to define my module variables at the top, which explains the purpose 
# of this init function, invoked at the bottom
def __init():
    helper = Helper(constants.plugin_name, argv=sys.argv)
    return helper


class Helper(shared_helper.Helper):		
    def debug_decrypt_key(self):		
        return (helper.get_setting('debug-decryption-key'))

    def domain_url(self):
        return '%s://%s' % (helper.get_setting('http-type'), constants.domain)

    def handle_html_errors(self, html, e):		
        if html == '':		
            self.show_error_dialog(['',str(e)])           
            #if e.args[0] == 'The service is unavailable.':		
            #    self.log_debug('The service is unavailable.')		
            #    self.show_error_dialog(['Kissanime is reporting that their service is currently unavailable.','','Please try again later.'])		
            #elif e.args[0] == "You're browsing too fast! Please slow down.":		
            #    self.log_debug('Got the browsing too fast error 1.')		
            #    self.show_error_dialog(["Kissanime is reporting that you're browsing too quickly.",'','Please wait a bit and slow down :)'])		
            #else:		
            #    import urllib2		
            #    self.log_debug('Failed to grab HTML' + ('' if e == None else ' with exception %s' % str(e)))		
            #    if isinstance(e, urllib2.HTTPError) and e.code == 503:		
            #        self.show_error_dialog(['The service is currently unavailable.', '', 'If it does not respond after 1 more try, the site may be temporarily down.'])		
            #    else:		
            #        self.show_error_dialog([		
            #            'Failed to parse the KissAnime website.',		
            #            '',		
            #            ('Error details: %s' % str(e))		
            #            ])		
        elif html == "You're browsing too fast! Please slow down.":		
            self.log_debug('Got the browsing too fast error.')		
            self.show_error_dialog(["Kissanime is reporting that you're browsing too quickly.",'','Please wait a bit and slow down :)'])		
            html = ''		
        elif html == 'Not found':		
            self.log_debug('Navigated to a dead page')		
            self.show_error_dialog(['This page does not exist.', '', 'If you clicked on a related link, KissAnime sometimes autogenerates related links which do not exist.'])		
            html = ''		
        return html


helper = __init()