from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_2 import *
'''
    @post list
    method : GET
    url_0 =  https://www.wonju.go.kr/www/selectCtyhllCldrList.do?key=213&searchLgd=1&bgnde={}&endde={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.channel_main_url + href
    header :
        None
'''
'''
https://www.wonju.go.kr/www/selectCtyhllCldrList.do?key=213&searchLgd=1&bgnde=2021-01-01&endde=2021-12-31
https://www.wonju.go.kr/www/selectCtyhllCldrList.do?key=213&searchLgd=1&bgnde=2022-01-01&endde=2022-12-31
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '원주시청'
        self.post_board_name = '주요문화행사'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.session = set_headers(self.session)
        self.page_count = 1
        self.channel_main_url = 'https://www.wonju.go.kr/www'
        while True :
            if self.page_count == 1:
                self.channel_url = self.channel_url_frame.format('2021-01-01', '2021-12-31')
            elif self.page_count == 2:
                self.channel_url = self.channel_url_frame.format('2022-01-01', '2022-12-31')
            else:
                break
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