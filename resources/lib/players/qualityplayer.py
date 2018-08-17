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
from resources.lib.common.webpage import WebPage
from resources.lib.common.args import args
from resources.lib.players.videoplayer import VideoPlayer
import xbmcgui, re
from resources.lib.common.nethelpers import net, cookies

#Addon = xbmcaddon.Addon(id='plugin.video.unofficialkissanime') 
#sys.path.append(os.path.join(Addon.getAddonInfo('path'), r'resources', r'lib'))


class QualityPlayer(WebPage, VideoPlayer):
    def __init__(self, url=''):
        WebPage.__init__(self)
        VideoPlayer.__init__(self, url)
        self.net, self.cookies = net, cookies	
        self.id = args.value.split('id=')[-1]		
        self.form_data = {}
		
        self.form_data ={'eID': self.id}
        self.html = ''
        self.html, e = self.net.get_html(helper.domain_url() + '/Mobile/GetEpisode', self.cookies, helper.domain_url(),	self.form_data)
        self.html = helper.handle_html_errors(self.html, e)		
						
    ''' PUBLIC FUNCTIONS '''
    def determine_quality(self):
        helper.start('QualityPlayer.determine_quality')
		
        #helper.show_error_dialog(['',str(self.html)])			
        #self.link = self.html.split('|||')[0]
        target = self.html.split('|||')[0]
        target = target.replace('www.rapidvideo.com/e/','www.rapidvideo.com/?v=')         
        params_url,e = self.net.get_html( '%s&q=360p' % target, self.cookies, helper.domain_url())
        quali = re.findall(r'&q=(.*?)"',params_url)
        quali = quali[::-1]				
        quali_choser = helper.present_selection_dialog('Choose the quality from the options below', quali) 
        if ( quali_choser != -1):		
            params_url,e = self.net.get_html('%s&q=%s' % (target, quali[quali_choser]), self.cookies, helper.domain_url())				
            target = re.search('<source\ssrc=\"([^\"]+)\"\s.+title=\"([^\"]+)\"\s.+?>', params_url).group(1) #',\ssrc: \"([^\"]+?)\"' 
            #helper.show_error_dialog(['',str(target)])					
            helper.resolve_url(target)
        target = ''		
		
		
        #links = self.__get_quality_links()
        #if len(links) == 0:
        #    return
        #if helper.get_setting('preset-quality') == 'Individually select':
        #    quality_options = [item[0] for item in links]
        #    idx = helper.present_selection_dialog('Choose the quality from the options below', quality_options)
        #    if idx != -1:
        #        self.link = links[idx][1]
        #else:
        #    self.link = self.__get_best_link_for_preset_quality(links)
        helper.log_debug('the chosen link: %s' % self.link)
        helper.end('QualityPlayer.determine_quality')

    ''' PROTECTED FUNCTIONS '''
    def _decode_link(self, url):

        if not url:
            return None

        if 'https://' in url or 'http://' in url:
            decoded_link_val = url # Openload probably, since it's already a valid link
        else:
            helper.log_debug('URL to decode: %s' % url)
            try:
                decoded_link_val = self.__decrypt_link(url)#.decode('base64'))
                helper.log_debug('Decoded URL: %s' % decoded_link_val)
            except Exception as e:
                decoded_link_val = None
                helper.log_debug('Failed to decode the link with exception %s' % str(e))

        return decoded_link_val

    ''' PRIVATE FUNCTIONS '''
    def __get_quality_links(self):
        if self.soup == None:
            return

        # Find the links
        raw_links = []
        quality_options = self.soup.find(id="slcQualix") 
				
        if quality_options:
            helper.log_debug('Using KissAnime or Beta servers')
            raw_links = quality_options.find_all("option")  
			
        else:
            helper.log_debug('Could not find KissAnime server links; attempting to find Openload link')
            try:
                # The Openload link is the default video link
                video_str = self.__get_default_video_link()
                from bs4 import BeautifulSoup
                fake_soup = BeautifulSoup('<option value="%s">Openload</option>' % video_str, "html.parser")
                raw_links = fake_soup.find_all('option')
                helper.log_debug('Successfully found and parsed Openload link %s' % raw_links)
            except Exception as e:
                raw_links = []
                helper.log_debug('Failed to parse Openload link with exception: %s' % str(e))
                helper.show_error_dialog(['Could not find supported video link for this episode/movie'])

        # Process the links
        links = []
        for option in raw_links:
            quality = option.string			
			
            link_val = self._decode_link(option['value'])

            # If we failed to decode the link, then we'll just use the already selected option 
            # and ignore the rest
            if not link_val:
                helper.show_error_dialog(['Failed to decrypt any video links.  Videos with default Openload sources should still work.'])
                break

            links.append((quality, link_val))

        return links
    
    def __get_best_link_for_preset_quality(self, links):
        preset_quality = int(helper.get_setting('preset-quality').strip('p'))
        
        for link in links:
            quality = link[0]
            if quality == 'Openload' or preset_quality >= int(quality.replace('Default quality - ', '').strip('p')):
                helper.log_debug('Found media to play at matching quality: %s' % quality)
                url_to_play = link[1]
                break

        if url_to_play == None:
            helper.log_debug('No matching quality found; using the lowest available')
            url_to_play = links[-1]['value']

        return url_to_play

    def __get_default_video_link(self):
        video_str = self.html.split('#divContentVideo')[1].split('iframe')[1].split('src=')[1].split('"')[1]
        helper.log_debug('Got default video string: %s' % video_str)
        return video_str

    def __decrypt_link(self, url):
        iv = 'a5e8d2e9c1721ae0e84ad660c472c1f3'.decode('hex')        
					
        #strmn = '//storage//.kodi//addons//plugin.video.unofficialkissanime//testfile.log'
        #import xbmcvfs
        #file_desc = xbmcvfs.File(strmn, 'w')
        #result=file_desc.write(str(url))
        #file_desc.close() 
		
        if (helper.debug_decrypt_key() != ''):
            helper.log_debug('Using the key input from the debug settings')
            key = helper.debug_decrypt_key().decode('hex')
        else:
            helper.log_debug('Attempting to get key from html')
            key = self.__get_key_from_html()

        return self.__decrypt_text(key, iv, url.decode('base64'))

    def __decrypt_text(self, key, iv, txt):
        from resources.lib import pyaes
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv=iv))
        decrypted_txt = decrypter.feed(txt)
        decrypted_txt += decrypter.feed()
        return decrypted_txt

    def __get_key_from_html(self):
        # Find the last line to set skH, the seed to the key
        set_skH_dict = {}
        for filename in ['vr.js', 'skH = _']:
            set_skH_dict[filename] = self.html.rfind(filename)
        
        sorted_skH = sorted(set_skH_dict, key=set_skH_dict.get, reverse=True)
        last_set_skH_file = sorted_skH[0]
        last_set_skH_line = set_skH_dict[last_set_skH_file]

        skH = self.__get_base_skH(last_set_skH_file)

        # Find modifications after the last line that sets skH
        js_dict = {}
        for f in ['shal.js', 'moon.js', 'file3.js', 'skH +=', 'skH = skH +', 'skH = skH[']:
            line_num = self.html.find(f)
            if line_num > last_set_skH_line:
                js_dict[f] = self.html.find(f)

        # Sort and then apply modifications in order of appearance
        for filename in sorted(js_dict, key=js_dict.get, reverse=False):
            skH = self.__update_skH(skH, filename)

        import hashlib
        key = hashlib.sha256(skH).hexdigest()
        helper.log_debug('Found the decryption key: %s' % key)
        #xbmcgui.Dialog().ok('Warning',str(key.decode('hex')))        
        return key.decode('hex')

    def __get_base_skH(self, filename):
        if filename == 'vr.js':
            return 'nhasasdbasdtene7230asb'
        elif filename == 'skH = _':
            # We need to find the last skH before ovelwrap
            split1 = self.html.split("ovelWrap($('#slcQualix').val())")[0]
            split2 = split1.split('skH = _')[-2]
            obfuscated_list_str = '[' + split2.split('[')[-1].strip('; ')
            import ast
            obfuscated_list = ast.literal_eval(obfuscated_list_str)
            return obfuscated_list[0]
        else:
            helper.log_debug('Failed to recognize base skH file %s' % filename)
            return ''

    def __update_skH(self, skH, filename):
        if filename == 'shal.js':
            return skH + '6n23ncasdln213'
        elif filename == 'moon.js':
            return skH + 'znsdbasd012933473'
        elif filename == 'file3.js':
            return skH.replace('a', 'c')
        elif filename == 'skH +=':
            return skH + '6n23ncasdln213'
        elif filename == 'skH = skH +':
            return skH + 'znsdbasd012933473'
        elif filename == 'skH = skH[':
            return skH.replace('a', 'c')
        else:
            helper.log_debug('Failed to recognize skH modifier file %s' % filename)
            return skH