from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기도일자리재단 잡아바 지원정책
# 타겟 : 모든 포스트
# 중단 시점 : 컨텐츠가 없는 마지막페이지 도달시 중지

# HTTP Request
'''
    @post list 

    method : post
    url : https://www.jobaba.net/sprtPlcy/info/moreListAjax2020.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. srchRecordCountPerPage=50
        2. currentPageNo={page_count}
    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : fixed

'''
'''
    @post info

    method : get
    url : https://www.jobaba.net/fntn/dtl2020.do?seq={}.format(postSeq)

    header : 
        None
    body :
        None
    required data searching point :
        1. postSeq : post list parsing postSeq 
'''

isUpdate = True
sleep_sec = 3

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '잡아바'
        self.post_board_name = '지금 접수중인 정책'
        self.post_url =  'https://www.jobaba.net/fntn/dtl2020.do?seq={}'
        self.channel_main_url = 'https://www.jobaba.net'
    
    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)
        self.page_count = 1 
        while True:
            self.post_list_scraping()
            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break
    
    def post_list_scraping(self):
        data = {
            "srchRecordCountPerPage" : 50,
            "currentPageNo" : self.page_count
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)
