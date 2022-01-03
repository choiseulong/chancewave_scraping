from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 복지로

# 타겟 : 모든 포스트

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.bokjiro.go.kr/ssis-teu/TWAT52005M/twataa/wlfareInfo/selectWlfareInfo.do
    header :
        1. Content-Type: application/json; charset=UTF-8
        2. User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36

    body :
        1. "page":"{page_count}"
        2. "jjim":""
        3. "tabId":"1"
    required data searching point :
        header_1 : fixed
        header_2 : fixed
        body_1 : page_count
        body_2 : fixed
        body_3 : [1,2,3]
'''
'''
    @post info

    method : get
    url : 'post_url'
    header :
        None
'''

isUpdate = True
sleep_sec = 1
jsonize = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '복지로'
        self.post_board_name = '서비스 목록'
        self.post_url = "https://www.bokjiro.go.kr/ssis-teu/twataa/wlfareInfo/moveTWAT52011M.do?wlfareInfoId={}"
    
    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        self.additional_key_value.append(("Content-Type", "application/json; charset=UTF-8"))
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)
        for i in range(1,4):
            self.tabId = i
            while True :
                self.post_list_scraping()
                if not self.scraping_target:
                    break
                if self.scraping_target :
                    self.target_contents_scraping()
                    self.collect_data()
                    self.mongo.reflect_scraped_data(self.collected_data_list)
                    self.page_count += 1 

                else:
                    break

    def post_list_scraping(self):
        data = {
            "dmSearchParam" : {
                "page" : f"{self.page_count}",
                "jjim" : "",
                "tabId" : f"{self.tabId}"
            }
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec, jsonize)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)