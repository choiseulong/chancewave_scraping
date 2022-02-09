from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_1 import *

# 채널 이름 : 울주군청

#HTTP Request
'''
    @post list
    method : GET
    url_1 = https://www.ulju.ulsan.kr/ulju/bbs/list.do?ptIdx=149&mId=0404070000&\
        cancelUrl=%%2Fulju%%2Fbbs%%2Flist.do%%3FptIdx%%3D149%%26mId%%3D0404070000&page={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id)
    header :
        None
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '울주군청'
        self.post_board_name = '타기관소식'
        self.post_url = 'https://www.ulju.ulsan.kr/ulju/bbs/view.do?bIdx={}&ptIdx={}&mId={}'

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