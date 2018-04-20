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


from resources.lib.common.args import args
from resources.lib.common.helpers import helper
from bs4 import BeautifulSoup


class WebPage(object):
    def __init__(self, url_val=args.value, form_data=None):
        self.html = ''
        self.soup = None
        self.links = []
        self.has_next_page = False
        from resources.lib.common.nethelpers import net, cookies
        self.net, self.cookies = net, cookies

        user_agent = 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'	
        #scraper = cfscrape.get_tokens(helper.domain_url(),user_agent = user_agent)#cfscrape.create_scraper()
        
        #import cookielib		
        #ck = cookielib.Cookie(version=0, name='reqkey', value='rk1', port=None, port_specified=False,
		#domain='helper.domain()', domain_specified=False, domain_initial_dot=False, 
		#path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)		
        
        ##self.net._cj.clear(helper.domain(),'/','reqkey')
        
        #self.net._cj.set_cookie(ck)
        #self.net.save_cookies(self.cookies)		
				
		
        #helper.show_error_dialog(['',str(scraper[0]['cf_clearance'])]) 
        
        if not url_val:
            return

        url_val = self.__fix_up_url(url_val)
        url = url_val if 'http' in url_val else (helper.domain_url() + url_val)
        #helper.show_error_dialog(['',str(url)]) 
        #self.net._fetch(url, form_data) 		
        self.html, e = self.net.get_html(url, self.cookies, helper.domain_url(), form_data)
        #helper.show_error_dialog(['',str(self.html.encode('utf-8'))])
        self.html = helper.handle_html_errors(self.html, e)
        helper.log_debug('HTML is %sempty' % ('' if self.html == '' else 'not '))
        
        self.html = self._filter_html(self.html)
        self.soup = BeautifulSoup(self.html, "html.parser") if self.html != '' else None

    ''' PROTECTED FUNCTIONS '''
    def _filter_html(self, html):
        new_lines = []
        for line in html.split('\n'):
            if 'Please disable AdBlock' in line or "</scr'+'ipt>" in line:
                continue
            new_lines.append(line)
        html = '\n'.join(new_lines)
        return html

    ''' PRIVATE FUNCTIONS '''
    def __fix_up_url(self, url):
        import urllib
        # The net helper cannot handle unicode values in the URL, so let's remove those
        new_url = ''
        for c in url.decode('utf-8'):
            new_c = c.encode('utf-8')
            new_url += urllib.quote_plus(new_c) if ord(c) >= 0x80 else new_c
        return new_url