from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 문경시청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.gbmg.go.kr/portal/bbs/list.do?ptIdx=73&mId=0301010000&cancelUrl=%2Fportal%2Fbbs%2Flist.do%3FptIdx%3D73%26mId%3D0301010000&page={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gbmg.go.kr/portal/bbs/view.do?mId=0301010000&bIdx={postId}&ptIdx=73
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '문경시청'
        self.postBoardName = '새소식'
        self.channelMainUrl = 'https://www.gbmg.go.kr'
        self.postUrl = 'https://www.gbmg.go.kr/portal/bbs/view.do?mId=0301010000&bIdx={}&ptIdx=73'
        
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