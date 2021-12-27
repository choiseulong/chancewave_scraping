from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 금융위원회

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.fsc.go.kr/no010104?curPage={PageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : postUrl
    header :
        None
'''

sleepSec = 10
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '금융위원회'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.fsc.go.kr'
        
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


            

 



