from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 환경부

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  http://me.go.kr/home/web/board/list.do?boardMasterId=39&menuId=290&pagerOffset={(pageCount-1 * 10)}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://me.go.kr/home/web/board/read.do?menuId=290&boardId={postId}&boardMasterId=39
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '환경부'
        self.postBoardName = '공지 및 공고'
        self.channelMainUrl = 'http://me.go.kr'
        self.postUrl = 'https://me.go.kr/home/web/board/read.do?menuId=290&boardId={}&boardMasterId=39'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format((self.pageCount-1 * 10))
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