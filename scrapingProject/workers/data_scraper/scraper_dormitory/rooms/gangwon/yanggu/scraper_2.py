from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_2 import *

# 채널 이름 : 양구군청

#HTTP Request
'''
    @post list
    method : GET
    url_0 =  https://www.yanggu.go.kr/lll/yglll/pageview.do?url=sub02a&keyvalue=sub02
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
    post_url 이 없느 친구들 업데이트 이슈..
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '양구군평생학습관'
        self.post_board_name = '교육프로그램'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.session = set_headers(self.session)
        self.channel_url = self.channel_url_frame.format(self.page_count)
        self.post_list_scraping()
        if self.scraping_target :
            self.collect_data()
            self.mongo.reflect_scraped_data(self.collected_data_list)

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)
