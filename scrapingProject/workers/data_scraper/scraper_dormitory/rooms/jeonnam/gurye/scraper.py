from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 구례군청

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.gurye.go.kr/board/list.do;gurye.go.kr=2BDDE38561D7B54E4DEC94C93860235A?\
        bbsId=BBS_0000000000000056&menuNo=115004001000&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : self.channel_main_url + href
    header :
        None

'''
sleep_sec = 4
isUpdate = True

class Scraper(ABCScraper):

    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '구례군청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.gurye.go.kr'
        
    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
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