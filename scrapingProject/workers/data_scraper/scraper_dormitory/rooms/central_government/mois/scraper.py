from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 행정안전부

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.mois.go.kr/frt/bbs/type013/commonSelectBoardList.do?bbsId=BBSMSTR_000000000006&pageIndex={pageCount}
    header :
        1.Content-Type: application/x-www-form-urlencoded
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : https://www.mois.go.kr/frt/bbs/type013/commonSelectBoardArticle.do?bbsId={}&nttId={}
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.mois.go.kr'
        self.postUrl = 'https://www.mois.go.kr/frt/bbs/type013/commonSelectBoardArticle.do?bbsId={}&nttId={}'
        
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