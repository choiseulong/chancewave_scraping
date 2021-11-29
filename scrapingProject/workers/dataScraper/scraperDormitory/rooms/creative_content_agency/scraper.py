from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 한국콘텐츠진흥원

# 타겟 : 모든 포스트
# 중단 시점 : 등록일 기준 이전 포스트가 존재하지 않을 시
# ** 첫페이지만 존재하여 추후 수정 필요

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.kocca.kr/cop/pims/list.do?menuNo=200828&recptSt=
    header :
        None
'''
'''
    @post info
    method : GET
    url : 'postUrl'
    header :
        None
'''

isUpdate = True
sleepSec = 2

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.kocca.kr/'
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.post_list_scraping()
        if self.scrapingTarget :
            self.target_contents_scraping()
            self.collect_data()
            self.mongo.reflect_scraped_data(self.collectedDataList)

    def post_list_scraping(self):
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)
    



            

 

