from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 제주

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시


#HTTP Request
'''
    @post list

    method : GET
    url = https://www.jeju.go.kr/news/news/news.htm?page={pageCount}
    header :
        User-Agent
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : postUrl
    header :
        None
'''

sleepSec = 3
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '제주특별자치도'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.jeju.go.kr'
        
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
            
            if self.pageCount == 4 :
                break
            
 
    def post_list_scraping(self):
        postBoardNameInfo = {
            'jeju_1' : '일자리/중소기업 알림마당',
            'jeju_2' : '일자리지원정책 알림마당',
            'jeju_3' : '평생교육강좌(민간)',
            'jeju_4' : '여성교육정보(민간)',
            'jeju_5' : '문화역사 알림마당'

        }
        if self.channelCode in postBoardNameInfo.keys():
            self.postBoardName = postBoardNameInfo[self.channelCode]
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)


            

 



