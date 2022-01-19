from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_1 import *

# 채널 이름 : 대전동구청

#HTTP Request
'''
    @post list
    method : GET
    url_1 = https://www.donggu.go.kr/lll/damoa/contents/learning/community/01\
        /community.01.001.motion?mnucd=MENU0100020&bmode=list&pageIndex={}
    header :
        None
'''
'''
    @post info
    method : POST
    url : 
        self.post_url
    header :
        None
    body:
        
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '대전동구청'
        self.post_board_name = '학습커뮤니티_공지사항'
        self.post_url = 'https://www.donggu.go.kr/lll/damoa/contents/learning/community/01/community.01.001.motion'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True :
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()
            if self.scraping_target :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)