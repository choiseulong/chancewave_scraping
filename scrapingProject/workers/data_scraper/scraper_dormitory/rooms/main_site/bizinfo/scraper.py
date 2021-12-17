from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 기업마당

# 타겟 : 모든 포스트
# 중단 시점 : 등록일 기준 이전 포스트가 존재하지 않을 시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.bizinfo.go.kr/see/seea/selectSEEA100.do
    header :
        1. Content-Type: application/x-www-form-urlencoded
    body :
        1. "pageIndex":{pageCount}
    required data searching point :
        header_1 : fixed
        body_1 : pageCount
'''
'''
    @post info
    method : GET
    url : 'postUrl'
    header :
        None
'''

isUpdate = True
sleepSec = 3

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '기업마당'
        self.postBoardName = '지원사업조회'
        self.postUrl = "https://www.bizinfo.go.kr/see/seea/selectSEEA140Detail.do?pblancId={}&menuId=80001001001"
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        while True :
            self.pageCount += 1 
            self.post_list_scraping()
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
            else:
                break
            
            if self.pageCount == 5 :
                break

    def post_list_scraping(self):
        data = {
            "pageIndex" : self.pageCount
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)