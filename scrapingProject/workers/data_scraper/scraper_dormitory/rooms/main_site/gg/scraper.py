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
        2. offset={(page_count-1)*12}
    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : page_count
'''
'''
    @post info

    method : GET
    url : post_url
    header : 
        None
    body :
        None
'''


is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '경기도청'
        self.post_board_name = '경기도 통합공모'
        self.post_url =  'https://www.gg.go.kr/bbs/boardView.do?bIdx={}&bsIdx=731&menuId=2916'
        self.channel_main_url = 'https://www.gg.go.kr/'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additional_key_value, is_update)
        self.page_count = 1
        while True :
            self.post_list_scraping()
            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
                if len(self.scraping_target) < 12:
                    break  
    
    def post_list_scraping(self):
        data = {
            "bsIdx" : 731,
            "offset" : (self.page_count-1) * 12
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(post_content_parsing_process)
