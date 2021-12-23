from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 칠곡군청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.cheongdo.go.kr/open.content/ko/administration/news/notice/?p={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.usc.go.kr/board/detail.tc?mn=1275&viewType=sub&mngNo=275&pageIndex=1&boardName=EOVYRHDWL&boardNo={posrId}&pageSeq=1314
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '칠곡군청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.cheongdo.go.kr'
        self.postUrl = 'https://www.chilgok.go.kr/portal/bbs/view.do?mId=0201010000&bIdx={}&ptIdx=111'
        
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