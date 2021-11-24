from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 마이홈


# 타겟 : 유효 일자 내의 포스트
# 중단 시점 : 모든 공고가 모집 완료인 시점에서 종료

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcList.do
    header :
        1. Content-Type : application/x-www-form-urlencoded; charset=UTF-8
    body :
        1. pageIndex={pageCount}
        2. srchSuplyTy=
    required data searching point :
        header_1 : fixed
        body_1 : pageCount
        body_2 : fixed
'''
'''
    @post info

    method : get
    url : 'postUrl'
    header :
        None
'''

isUpdate = True
sleepSec = 4

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId={}"
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        # post list 
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 1
        while True :
            self.post_list_scraping()
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else:
                break

    def post_list_scraping(self):
        data = {
            "pageIndex" : self.pageCount,
            "srchSuplyTy" : ""
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)
    



            

 

