from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 공정거래위원회

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.ftc.go.kr/www/cop/bbs/selectBoardList.do?key=13
    header :
        1. Content-Type: application/x-www-form-urlencoded
    body : 
        1. bbsId=BBSMSTR_000000002424
        2. bbsTyCode=BBST01
        3. pageIndex=1

    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : fixed
        body_3 : pageCount

'''
'''
    @post info
    method : GET
    url : https://www.mpva.go.kr/mpva/selectBbsNttView.do?key=76&bbsNo=15&nttNo={postNumber}
    header :
        None
    required data searching point :
        header_1 : fixed
'''

sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.ftc.go.kr'
        self.postUrl = 'https://www.ftc.go.kr/www/cop/bbs/selectBoardArticle.do?key=13'
        
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

            if self.pageCount == 3 :
                break

    def post_list_scraping(self):
        data = {
            "bbsId" : "BBSMSTR_000000002424",
            "bbsTyCode" : "BBST01",
            "nttId" : 0,
            "pageIndex" : self.pageCount
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)


            

 



