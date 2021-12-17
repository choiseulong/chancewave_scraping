from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 식품의약품안전처

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.mfds.go.kr/brd/m_74/list.do?page={pageCount}
    header :
        None
'''
'''
    @post info
    method : GET
    url : https://www.mpva.go.kr/mpva/selectBbsNttView.do?key=76&bbsNo=15&nttNo={postNumber}
    header :
        None
    required data searching point :
        header_1 : fixed
'''

sleepSec = 3

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.mfds.go.kr'
        self.postUrl = 'https://www.mfds.go.kr/brd/m_74/view.do?seq={}'
        
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
        if self.channelCode == 'mfds_1':
            self.postUrl = 'https://www.mfds.go.kr/brd/m_689/view.do?seq={}'

        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)


            

 



