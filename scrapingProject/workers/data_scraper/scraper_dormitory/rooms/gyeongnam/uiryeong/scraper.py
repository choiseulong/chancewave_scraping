from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 의령군청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  http://www.uiryeong.go.kr/board/list.uiryeong?boardId=BBS_0000085&menuCd=DOM_000000403001001000&orderBy=REGISTER_DATE%20DESC&startPage={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.uiryeong.go.kr/board/view.uiryeong?boardId=BBS_0000085&menuCd=DOM_000000403001001000&dataSid=548690={postId}
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '의령군청'
        self.postBoardName = '군정소식'
        self.channelMainUrl = 'http://www.uiryeong.go.kr'
        self.postUrl = 'http://www.uiryeong.go.kr/board/view.uiryeong?boardId=BBS_0000085&menuCd=DOM_000000403001001000&dataSid={}'
        
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