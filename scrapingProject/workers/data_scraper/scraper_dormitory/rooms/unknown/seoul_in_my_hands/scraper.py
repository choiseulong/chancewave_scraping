from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# HTTP Request
'''
    @post list 

    method : post
    url : https://mediahub.seoul.go.kr/competition/competitionListAjax.do
    header : 
        1. User-Agent
        2. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. search_pageNo={pageCount}
        2. search_contestStatus=all
    required data searching point :
        header_1 : fixed
        header_2 : fixed
        body_1 : Make pageCount loop
        body_2 : fixed
'''
'''
    @post info

    method : get
    url : https://mediahub.seoul.go.kr/gongmo/{postSeq}

    header : 
        1. User-Agent
    body :
        None
    required data searching point :
        header_1 : fixed 
'''

isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl =  'https://mediahub.seoul.go.kr/gongmo/{}'
        self.channelMainUrl = 'https://mediahub.seoul.go.kr'

    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 1
        while True :
            self.post_list_scraping()
            if self.scrapingTarget:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else :
                break
    
    def post_list_scraping(self):
        data = {
            "search_pageNo" : self.pageCount,
            "search_contestStatus" : "all"
        }
        super().post_list_scraping(postListParsingProcess, 'post', data)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(postContentParsingProcess)
