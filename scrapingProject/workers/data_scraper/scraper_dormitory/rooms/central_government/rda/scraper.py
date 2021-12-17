from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 농촌진흥청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.rda.go.kr/board/board.do?prgId=nei_ancmttEntry&currPage={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.rda.go.kr/board/board.do?boardId=ancmtt&prgId=nei_ancmttEntry&dataNo={postId}
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '농촌진흥청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.rda.go.kr'
        self.postUrl = 'https://www.rda.go.kr/board/board.do?boardId=ancmtt&prgId=nei_ancmttEntry&menu_id=pun&currPage=1&dataNo={}&mode=updateCnt'
        
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
            "page" : self.pageCount,
            "row" : 50
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)