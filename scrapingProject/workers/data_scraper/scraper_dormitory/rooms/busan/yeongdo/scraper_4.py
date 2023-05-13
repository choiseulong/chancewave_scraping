from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_4 import *
'''
    @post list
    method : GET
    url =   https://www.yeongdo.go.kr/hll/01419/01420.web?gcode=1146&cpage={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url + href
    header :
        None

'''

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산영동구평생학습관'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.yeongdo.go.kr/hll/01419/01420.web'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
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
        sleep_sec = 1
        if '9' in self.channel_code:
            sleep_sec = 2
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        sleep_sec = 1
        if '9' in self.channel_code:
            sleep_sec = 2
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)