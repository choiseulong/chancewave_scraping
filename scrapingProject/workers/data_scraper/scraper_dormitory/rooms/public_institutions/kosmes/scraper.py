from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 중소벤처기업진흥공단

#HTTP Request
'''
    @post list
    method : POST
    url_0 = http://kosmes.or.kr/sh/nts/notice_list.json
    header :
        Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body :
        1. nowPage = {page_count}
        2. param = 'proc=List'
'''
'''
    @post info
    method : POST
    url : 
        self.post_url
    header :
        1. "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
    body : 
        {
            "searchG":"titleCon",
            "param":"proc=View",
            "seqNo":post_id
        }
'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '중소벤처기업진흥공단'
        self.post_board_name = '공지사항'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.post_url = channel_url
        self.page_count = 1
        while True :
            self.session = set_headers(self.session)
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()
            if self.scraping_target :
                self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
                self.session = set_headers(self.session, self.additional_key_value, is_update)
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break

    def post_list_scraping(self):
        data = {
            'nowPage' : self.page_count,
            'param' : 'proc=List'
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)