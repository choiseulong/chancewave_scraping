from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
from workers.dataScraper.parser.seoul_welfare_portal import *
from workers.dataServer.mongoServer import MongoServer
from .seoul_welfare_portal_0 import Scraper as default_scraper
import json 

'''
    method = POST
    body -> string {"content":"","startIndex":1,"endIndex":99999}
    headers -> Content-Type: application/json; charset=UTF-8
'''

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.extract_post_list_from_response_text = extract_post_list_from_response_text_other

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        self.session = set_headers([['Content-Type', 'application/json; charset=UTF-8']])
        pageCount = 1
        while True :
            self.post_list_scraping(channelCode, channelUrl)
            if self.scrapingTarget :
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else :
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
                break


    def post_list_scraping(self, channelCode, channelUrl):
        data = json.dumps(
            {"startIndex":1,"endIndex":99999}
        )
        status, response = post_method_response(self.session, channelUrl, data)
        if status == 'ok':
            self.scrapingTarget = self.extract_post_list_from_response_text(response.json(), self.dateRange, channelCode)
        else :
            raise Exception(f'scraping channel {channelCode} post list error')