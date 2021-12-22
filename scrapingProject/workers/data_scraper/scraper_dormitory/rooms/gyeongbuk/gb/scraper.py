from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경상북도청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.gb.go.kr/Main/page.do?URL=/common/board/board.do&mnu_uid=6786&BD_CODE=bbs_gongji&cmd=1&Start={(pageCount-1) * 10}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gb.go.kr/Main/page.do?mnu_uid=6786&BD_CODE=bbs_gongji&cmd=2&B_NUM={postId}&B_STEP=149047400&V_NUM=20059
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '경상북도청'
        self.postBoardName = '알림마당'
        self.channelMainUrl = 'https://www.gb.go.kr'
        self.postUrl = 'https://www.gb.go.kr/Main/page.do?mnu_uid=6786&BD_CODE=bbs_gongji&cmd=2&B_NUM={}&B_STEP={}&V_NUM=20059'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format((self.pageCount-1)*10)
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