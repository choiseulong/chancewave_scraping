from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 국가보훈처

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.mpva.go.kr/mpva/selectBbsNttList.do?key=76&bbsNo=15&pageIndex={pageCount}
    header :
        None
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : https://www.mpva.go.kr/mpva/selectBbsNttView.do?key=76&bbsNo=15&nttNo={postNumber}
    header :
        None
'''

sleepSec = 2

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.mpva.go.kr'
        self.postUrl = 'https://www.mpva.go.kr/mpva/selectBbsNttView.do?key=76&bbsNo=15&nttNo={}'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            self.post_list_scraping()
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else :
                break

    def post_list_scraping(self):
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)


            

 


