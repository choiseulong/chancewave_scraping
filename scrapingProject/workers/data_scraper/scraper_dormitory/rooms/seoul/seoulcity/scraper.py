from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름
# seoul_city_0 : 분야별 새소식
# seoul_city_1 : 이달의 행사 및 축제
# seoul_city_2 : 이벤트 신청

# 타겟 : 유효 일자 내의 포스트
# 중단 시점 : 데이터의 개수가 0개인 페이지에 도달할 경우

#HTTP Request
'''
    @post list

    method : post
    url = https://www.seoul.go.kr/realmnews/in/list.do
    header :
        1. User-Agent
    body :
        1. fetchStart = {page_count}
    required data searching point :
        header_1 : fixed
        body_1 : page_count
'''
'''
    @post info

    method : get
    url : 'post_url'
    header :
        None
'''
class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '서울시청'
        self.post_board_name = '분야별 새소식'

    def get_post_body_post_list_page(self, num=1):
        data = {
            "fetchStart" : num
        }
        return data
    
    def scraping_process(self, channel_code, channel_url):
        super().scraping_process(channel_code, channel_url)
        
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
            "fetchStart" : self.page_count
        }
        if self.channel_code == 'seoul_city_1':
            self.post_board_name = '이달의 행사 및 축제'
        elif self.channel_code == 'seoul_city_2':
            self.post_board_name = '이벤트 신청'

        super().post_list_scraping(post_list_parsing_process, 'post', data)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process)
    



            

 

