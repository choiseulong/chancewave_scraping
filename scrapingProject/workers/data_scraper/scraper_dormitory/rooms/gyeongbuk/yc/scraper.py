from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 영천시청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.yc.go.kr/portal/bbs/list.do?ptIdx=544&mId=0301010000?cancelUrl=%%2Fportal%%2Fbbs%%2Flist.do%%3FptIdx%%3D544%%26mId%%3D0301010000&page={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.yc.go.kr/portal/bbs/view.do?bIdx={postId}&ptIdx=544&mId=0301010000
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '영천시청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.yc.go.kr'
        self.postUrl = 'https://www.yc.go.kr/portal/bbs/view.do?bIdx={}&ptIdx=544&mId=0301010000'
        
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