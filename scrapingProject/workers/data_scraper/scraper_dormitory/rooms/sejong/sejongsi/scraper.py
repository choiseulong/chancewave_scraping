from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 세종시

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.sejong.go.kr/bbs/R0071/list.do
    header :
        Accept-Encoding: gzip, deflate, br
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : postUrl
    header :
        Accept-Encoding: gzip, deflate, br
    required data searching point :
        header_1 : fixed
'''

sleepSec = 3
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '세종시청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.sejong.go.kr'
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(['Accept-Encoding', 'gzip, deflate, br'])
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 1
        while True :
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
            "pageIndex" : self.pageCount
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)


            

 



