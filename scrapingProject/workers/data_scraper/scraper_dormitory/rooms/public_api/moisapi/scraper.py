from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 행정안전부 대한민국 공공서비스 정보

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://api.odcloud.kr/api/gov24/v1/serviceList?perPage=20&serviceKey={}&page={}
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
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.api_key = '9R1Mmq8MdmV/tc8/GgmL7wXkDFcSCCR47D/oGdcXM3gB9uhW9mLUKCxdURGllAVViWqDqFlr7IC1SAXC22GLhQ=='
        self.channel_name = '행정안전부 대한민국 공공서비스 정보'
        self.post_url ='https://api.odcloud.kr/api/gov24/v1/serviceDetail?page=1&perPage=10&serviceKey={}&cond%5BSVC_ID%3A%3AEQ%5D={}'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.channel_url_frame = channel_url.replace('{}', self.api_key, 1)
        self.post_url = self.post_url.replace('{}', self.api_key, 1)
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