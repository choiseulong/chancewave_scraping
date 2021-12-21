from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경상남도

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.gyeongnam.go.kr/board/list.gyeong?boardId=BBS_0000057&menuCd=DOM_000000104001001000&paging=ok&startPage={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gyeongnam.go.kr/board/view.gyeong?boardId=BBS_0000057&menuCd=DOM_000000104001001000&paging=ok&dataSid={postId}
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '경상남도청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.gyeongnam.go.kr'
        self.postUrl = 'https://www.gyeongnam.go.kr/board/view.gyeong?boardId=BBS_0000057&menuCd=DOM_000000104001001000&paging=ok&dataSid={}'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            self.post_list_scraping()
            if self.scrapingTarget :
                if self.channelCode != 'gyeongnamdo_1':
                    self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else :
                break

    def post_list_scraping(self):
        if self.channelCode == 'gyeongnamdo_1':
            self.postBoardName = '팝업존'
            postListParsingProcess = postListParsingProcess_1
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)