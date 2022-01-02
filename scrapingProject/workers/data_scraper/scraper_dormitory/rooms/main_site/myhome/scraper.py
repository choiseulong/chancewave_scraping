from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 마이홈


# 타겟 : 모집중인 공고
# 중단 시점 : 모든 공고가 모집 완료인 시점에서 종료

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcList.do
    header :
        1. Content-Type : application/x-www-form-urlencoded; charset=UTF-8
    body :
        1. pageIndex={page_count}
        2. srchSuplyTy=
    required data searching point :
        header_1 : fixed
        body_1 : page_count
        body_2 : fixed
'''
'''
    @post info

    method : get
    url : 'post_url'
    header :
        None
'''

isUpdate = True
sleep_sec = 2

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '마이홈'
        self.post_board_name = '입주자모집공고'
        self.post_url = "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId={}"
    
    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)
        self.page_count = 1
        while True :
            self.post_list_scraping()
            if self.scraping_target :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else:
                break

    def post_list_scraping(self):
        data = {
            "pageIndex" : self.page_count,
            "srchSuplyTy" : ""
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)
    



            

 

