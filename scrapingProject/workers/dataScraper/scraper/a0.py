from ..scraperTools.tools import *
from ..parser.a0 import * 

'''
    required :
        headers :
            User-Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36
        body : 
            {"fetchStart" : Number}
'''
class Scraper:
    def __init__(self, session, channelCode, channelUrl):
        self.session = session
        self.channelCode = channelCode
        self.channelUrl = channelUrl
    
    def get_headers(self):
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        return headers
    
    def get_post_body_post_list_page(self, num=1):
        data = {
            "fetchStart" : num
        }
        return data

    def scraping_response(self, session, channelCode, channelUrl):
        headers = self.get_headers()
        data = self.get_post_body_post_list_page()
        status, response = post_method_response(session, channelUrl, headers, data)
        if status == 200 :
            post_list_parsing(response.text)
        print(status, response.text)

