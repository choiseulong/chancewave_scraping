from workers.dataScraper.parser.channel_b import *
from workers.dataServer.mongoServer import MongoServer

'''
    required in headers
    User-Agent: ''
'''


class Scraper:
    def __init__(self, session):
        self.session = session
        self.dateRange = []
    
    def get_headers(self):
        headers = {
            "User-Agent" : ""
        }
        return headers

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.session.headers = self.get_headers()
        mongo = MongoServer()
        self.dateRange = dateRange
        pageCount = 1
        while True :
            channelUrl = channelUrl.format(pageCount)
            self.postListResult = self.search_post_list(channelCode, channelUrl)
            pageCount += 1
            break
    
    def search_post_list(self, channelCode, channelUrl):
        contentsResultList = []
        status, response = get_method_response(self.session, channelUrl)
        if status == 'ok':
            result = b0_extract_post_list_from_response_text(response.text, self.dateRange)
            return result 
        else :
            raise Exception(f'scraping channel {channelCode} post list error')
          


        
# 상세 페이지는 post
# 제목 href속에있는 것들을 사용해서 요청
# body
# bbscttSn=13859&fileyn=N

# heaader
# Content-Type: application/x-www-form-urlencoded
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36
