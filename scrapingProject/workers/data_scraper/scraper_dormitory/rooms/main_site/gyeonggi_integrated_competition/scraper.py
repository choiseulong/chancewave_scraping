from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기도청 통합공모
# 타겟 : 모든 포스트
# 중단 시점 : 데이터 개수가 12개 미만으로 들어오는 페이지에 도달할 경우

# HTTP Request
'''
    @post list 

    method : post
    url : https://www.gg.go.kr/ajax/board/getList.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. bsIdx=731
        2. offset={(pageCount-1)*12}
    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : pageCount
'''
'''
    @post info

    method : GET
    url : https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId={pblancId} 
    header : 
        None
    body :
        None
'''


isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl =  'https://www.gg.go.kr/bbs/boardView.do?bIdx={}&bsIdx=731&menuId=2916'
        self.channelMainUrl = 'https://www.gg.go.kr/'

    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 1
        while True :
            self.post_list_scraping()
            if self.scrapingTarget:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
                if len(self.scrapingTarget) < 12:
                    break  
    
    def post_list_scraping(self):
        data = {
            "bsIdx" : 731,
            "offset" : (self.pageCount-1) * 12
        }
        super().post_list_scraping(postListParsingProcess, 'post', data)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(postContentParsingProcess)
