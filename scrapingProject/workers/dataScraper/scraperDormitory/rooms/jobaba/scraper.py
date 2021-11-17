from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# HTTP Request
'''
    @post list 

    method : post
    url : https://www.jobaba.net/sprtPlcy/info/moreListAjax2020.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. srchRecordCountPerPage=100000
        2. currentPageNo=1
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

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl =  'https://www.jobaba.net/fntn/dtl2020.do?seq={}'
        self.channelMainUrl = 'https://www.jobaba.net'
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded "))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.post_list_scraping()
        self.target_contents_scraping()
        self.collect_data()
        self.mongo.reflect_scraped_data(self.collectedDataList)
    
    def post_list_scraping(self):
        data = {
            "srchRecordCountPerPage" : 10000,
            "currentPageNo" : 1
        }
        super().post_list_scraping(postListParsingProcess, 'post', data)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(postContentParsingProcess)
