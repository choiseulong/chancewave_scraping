from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 창업넷

# 타겟 : 모집중인 공고
# 중단 시점 : 모집중인 공고가 존재하지 않는 마지막 지점 도달 시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701
    header :
        1. User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
    body :
        None
    required data searching point :
        header_1 : fixed
'''
'''
    @post info

    method : POST
    url : https://www.k-startup.go.kr/common/announcement/announcementDetail.do
    header :
        1. Content-Type: application/x-www-form-urlencoded
        2. User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
        3. Cookie: JSESSIONID=iEf7mwPfUncsKKe4yoHTDgmKUTOTLSBDVE5ydQjoypPYKPDvpN2dyEvVTDL1Iiwo.was1_servlet_kstartup02;

    body :
        1. CSRF_NONCE
        2. mid=30004
        3. searchPrefixCode=BOARD_701_001
        4. searchPostSn
    required data searching point :
        header_1 : fixed
        header_2 : fixed
        header_3 : fixed
        body_1 : @post list input 태그 value "CSRF_NONCE"
        body_2 : fixed
        body_3 : fixed
        body_4 : @post list a 태그 href 

'''

sleepSec = 3

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://www.k-startup.go.kr/common/announcement/announcementDetail.do'
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.post_list_scraping()
        if self.scrapingTarget :
            if not self.CSRF_TOKEN:
                self.CSRF_TOKEN = self.scrapingTarget[-1]
                del self.scrapingTarget[-1]
            self.target_contents_scraping()
            self.collect_data()
            self.mongo.reflect_scraped_data(self.collectedDataList)

    def post_list_scraping(self):
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)
    
