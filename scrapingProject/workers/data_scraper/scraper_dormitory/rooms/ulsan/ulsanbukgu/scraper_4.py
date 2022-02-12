from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_4 import *

# 채널 이름 : 울산북구청

#HTTP Request
'''
    @post list
    method : GET
    url =  https://www.bukgu.ulsan.kr/edu/join/join1.jsp?pagenum={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : self.channel_main_url + href
    header :
        None

'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '울산북구청'
        self.post_board_name = '주민자치센터프로그램'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True :
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()
            if self.scraping_target :
                # self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    # def target_contents_scraping(self):
    #     super().target_contents_scraping(post_content_parsing_process, sleep_sec)