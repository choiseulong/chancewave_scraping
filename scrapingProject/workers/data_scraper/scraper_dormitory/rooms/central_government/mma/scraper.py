from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 병무청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url =  https://www.mma.go.kr/board/boardList.do
    header :
        1.Content-Type: application/x-www-form-urlencoded
    body :
        1. pageUnit = 50
        2. pageIndex = {pageCount}
        3. gesipan_id = 2
    required data searching point :
        header_1 : fixed
        body_1 = fixed
        body_2 = pageCount
        body_3 = fixed
'''
'''
    @post info
    method : GET
    url : https://www.mma.go.kr/board/boardView.do?gesipan_id=2&gsgeul_no={postId}
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '병무청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.mma.go.kr'
        self.postUrl = 'https://www.mma.go.kr/board/boardView.do?gesipan_id=2&gsgeul_no={}'
        
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
        data = {
            "pageUnit" : 50,
            "pageIndex" : self.pageCount,
            "gesipan_id" : 2
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)