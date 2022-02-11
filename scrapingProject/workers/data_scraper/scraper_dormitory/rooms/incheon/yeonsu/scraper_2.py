from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_2 import *

# 채널 이름 : 연수구청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.yeonsu.go.kr/main/guidance/popupzone.asp
    header :
        None
'''
'''
    1페이지 뿐
    url 링크가 여러 채널로 퍼져서 진행하지 않음
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '연수구청'
        self.post_board_name = '연수소식 모아보기'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.channel_url = self.channel_url_frame.format(self.page_count)
        self.post_list_scraping()
        self.collect_data()
        self.mongo.reflect_scraped_data(self.collected_data_list)

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)