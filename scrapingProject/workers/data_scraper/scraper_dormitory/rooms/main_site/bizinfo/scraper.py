from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 기업마당

# 타겟 : 모든 포스트
# 중단 시점 : 등록일 기준 이전 포스트가 존재하지 않을 시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.bizinfo.go.kr/see/seea/selectSEEA100.do
    header :
        1. Content-Type: application/x-www-form-urlencoded
    body :
        1. "pageIndex":{page_count}
    required data searching point :
        header_1 : fixed
        body_1 : page_count
'''
'''
    @post info
    method : GET
    url : 'post_url'
    header :
        None
'''
'''
    update 23.05.01
    @post list

    method : GET
    url = https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?cpage={}
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

is_update = True
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '기업마당'
        # self.post_board_name = '지원사업조회'
        # self.post_url = "https://www.bizinfo.go.kr/see/seea/selectSEEA140Detail.do?pblancId={}&menuId=80001001001"
        self.post_board_name = '지원사업 공고'
        self.post_url = "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/{}"
    
    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        # self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additional_key_value, is_update)
        while True :
            self.page_count += 1 
            self.post_list_scraping()
            if self.scraping_target :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
            else:
                break

    def post_list_scraping(self):
        # data = {
        #     "pageIndex" : self.page_count
        # }
        # super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)
        self.channel_url = self.channel_url_frame.format(self.page_count)
        super().post_list_scraping(post_list_parsing_process, 'get')

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)