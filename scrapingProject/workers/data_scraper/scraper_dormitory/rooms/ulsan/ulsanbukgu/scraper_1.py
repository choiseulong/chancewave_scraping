from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_1 import *

# 채널 이름 : 울산북구청

#HTTP Request
'''
    @post list
    method : GET
    url = https://www.bukgu.ulsan.kr/lay1/bbs/S1T62C101/A/25/list.do?rows=10&cpage={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : self.post_url + href
    header :
        None

'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '울산북구청'
        self.post_board_name = '타기관소식'
        self.post_url = 'https://www.bukgu.ulsan.kr/lay1/bbs/S1T62C101/A/25/'

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