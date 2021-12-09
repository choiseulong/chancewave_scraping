from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 조달청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.pps.go.kr/kor/bbs/list.do?key=00641&pageIndex={pageCount}
    header :
        1. Content-Type: application/x-www-form-urlencoded
    required data searching point :
        header_1 : fixed

'''
'''
    @post info
    method : POST
    url : https://www.ftc.go.kr/www/cop/bbs/selectBoardArticle.do?key=13
    header :
        None
    body : 
        data = {
            "bbsId" : "BBSMSTR_000000002424",
            "bbsTyCode" : "BBST01",
            "nttId" : {nttId},
            "pageIndex" : self.pageCount
        }
    required data searching point :
        header_1 : fixed
        body_1 = {nttId}
'''

sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.pps.go.kr'
        self.postUrl = 'https://www.pps.go.kr/kor/bbs/view.do?bbsSn={}&key=00641'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)

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


            

 


