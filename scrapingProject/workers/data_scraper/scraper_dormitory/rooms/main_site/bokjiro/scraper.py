from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 복지로

# 타겟 : 모든 포스트
# 중단 시점 : 포스트가 존재하지 않는 마지막 지점 도달 시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.bokjiro.go.kr/ssis-teu/TWAT52005M/twataa/wlfareInfo/selectWlfareInfo.do
    header :
        1. Content-Type: application/json; charset=UTF-8
        2. User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36

    body :
        1. "page":"{pageCount}"
        2. "jjim":""
        3. "tabId":"1"
    required data searching point :
        header_1 : fixed
        header_2 : fixed
        body_1 : pageCount
        body_2 : fixed
        body_3 : [1,2,3]
'''
'''
    @post info

    method : get
    url : 'postUrl'
    header :
        None
'''

isUpdate = True
sleepSec = 3
jsonize = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = "https://www.bokjiro.go.kr/ssis-teu/twataa/wlfareInfo/moveTWAT52011M.do?wlfareInfoId={}"
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/json; charset=UTF-8"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        for i in range(1,4):
            self.tabId = i
            while True :
                self.pageCount += 1 
                self.post_list_scraping()
                if self.scrapingTarget :
                    self.target_contents_scraping()
                    self.collect_data()
                    self.mongo.reflect_scraped_data(self.collectedDataList)
                else:
                    break

    def post_list_scraping(self):
        data = {
            "dmSearchParam" : {
                "page" : f"{self.pageCount}",
                "jjim" : "",
                "tabId" : f"{self.tabId}"
            }
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec, jsonize)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)