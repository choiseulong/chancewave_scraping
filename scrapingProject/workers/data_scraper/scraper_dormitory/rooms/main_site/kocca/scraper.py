from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 한국콘텐츠진흥원

# 타겟 : 모든 포스트
# 중단 시점 : 마지막 페이지 도달 시

# ** 첫페이지만 존재하여 추후 수정 필요

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.kocca.kr/cop/pims/list.do?menuNo=200828&recptSt=
    url = https://www.kocca.kr/kocca/pims/list.do?menuNo=204104
    header :
        None
'''
'''
    @post info
    method : GET
    url : 'post_url'
    header :
        None
'''

sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '한국콘텐츠진흥원'
        self.post_board_name = '지원공고'#수정됨 지원사업 -> 지원공고
        self.channel_main_url = 'https://www.kocca.kr'
    
    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.post_list_scraping()
        if self.scraping_target :
            self.target_contents_scraping()
            self.collect_data()
            self.mongo.reflect_scraped_data(self.collected_data_list)

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)
