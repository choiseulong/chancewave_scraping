from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# HTTP Request
'''
    @post list 

    method : post
    url : https://mediahub.seoul.go.kr/competition/competitionListAjax.do
    header : 
        1. User-Agent
        2. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. search_pageNo={page_count}
        2. search_contestStatus=all
    required data searching point :
        header_1 : fixed
        header_2 : fixed
        body_1 : Make page_count loop
        body_2 : fixed
'''
'''
    @post info

    method : get
    url : https://mediahub.seoul.go.kr/gongmo/{postSeq}

    header : 
        1. User-Agent
    body :
        None
    required data searching point :
        header_1 : fixed 
'''

is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '내손안의서울'
        self.post_board_name = '공모전'
        self.post_url =  'https://mediahub.seoul.go.kr/gongmo/{}'
        self.channel_main_url = 'https://mediahub.seoul.go.kr'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additional_key_value, is_update)
        self.page_count = 1
        while True :
            self.post_list_scraping()
            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break
    
    def post_list_scraping(self):
        data = {
            "search_pageNo" : self.page_count,
            "search_contestStatus" : "all"
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(post_content_parsing_process)
