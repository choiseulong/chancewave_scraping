from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 중소기업유통센터

#HTTP Request
'''
    @post list
    method : GET
    url_0 =  https://www.sbdc.or.kr/board/notices
    header :
        None
    단일요청..
'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id) + href
    header :
        None
'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '중소기업유통센터'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.sbdc.or.kr/board/notice/{}'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.additional_key_value.append(("Accept", "application/json, text/plain, */*"))
        self.session = set_headers(self.session, self.additional_key_value, is_update)
        self.post_list_scraping()
        self.target_contents_scraping()
        self.collect_data()
        self.mongo.reflect_scraped_data(self.collected_data_list)

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)