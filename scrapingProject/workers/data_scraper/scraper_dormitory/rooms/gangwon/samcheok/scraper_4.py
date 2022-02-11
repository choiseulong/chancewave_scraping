from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_4 import *
'''
    @post list
    method : GET
    url_0 = https://www.samcheok.go.kr/specialty/00465/03090.web
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
'''
    이미지 요청시 Referer 로 post_url 전송 필요
    sleep_sec을 늘려야함
    페이지가 하나뿐
'''
sleep_sec = 10

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '삼척시청'
        self.post_board_name = '특성화사업'
        self.post_url = 'https://www.samcheok.go.kr/specialty/00465/03090.web'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.channel_url = self.channel_url_frame.format(self.page_count)
        self.post_list_scraping()
        if self.scraping_target :
            self.target_contents_scraping()
            self.collect_data()


    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)