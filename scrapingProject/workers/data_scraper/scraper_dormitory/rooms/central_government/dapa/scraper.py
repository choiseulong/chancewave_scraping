from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 방위사업청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url =  http://www.dapa.go.kr/dapa/na/ntt/selectNttList.do
    header :
        1.Content-Type: application/x-www-form-urlencoded
    body :
        1. currPage = {pageCount}
        2. bbsId = 443
    required data searching point :
        header_1 : fixed
        body_1 = pageCount
        body_2 = fixed
'''
'''
    @post info
    method : GET
    url : http://www.dapa.go.kr/dapa/na/ntt/selectNttInfo.do?bbsId=443&nttSn={postId}&menuId=356
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '방위사업청'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'http://www.dapa.go.kr'
        self.postUrl = 'http://www.dapa.go.kr/dapa/na/ntt/selectNttInfo.do?bbsId=443&nttSn={}&menuId=356'
        
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
        data = {
            "currPage" : self.pageCount,
            "bbsId" : 443
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)