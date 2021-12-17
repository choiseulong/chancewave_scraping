from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기도일자리재단 잡아바 지원정책
# 타겟 : 모든 포스트
# 중단 시점 : 컨텐츠가 없는 마지막페이지 도달시 중지

# HTTP Request
'''
    @post list 

    method : post
    url : https://www.jobaba.net/sprtPlcy/info/moreListAjax2020.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. srchRecordCountPerPage=50
        2. currentPageNo={pageCount}
    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : fixed

'''
'''
    @post info

    method : get
    url : https://www.jobaba.net/fntn/dtl2020.do?seq={}.format(postSeq)

    header : 
        None
    body :
        None
    required data searching point :
        1. postSeq : post list parsing postSeq 
'''

isUpdate = True
sleepSec = 6

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl =  'https://www.jobaba.net/fntn/dtl2020.do?seq={}'
        self.channelMainUrl = 'https://www.jobaba.net'
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 1 
        while True:
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
            "srchRecordCountPerPage" : 50,
            "currentPageNo" : self.pageCount
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(postContentParsingProcess, sleepSec)
