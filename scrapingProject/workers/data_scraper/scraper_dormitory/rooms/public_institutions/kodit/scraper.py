from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 신용보증기금

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.kodit.co.kr/kodit/na/ntt/selectNttList.do?sysId=kodit&menuTy=BBS\
        &cntntsId=148&menuId=2638&mi=2638&bbsId=148&currPage={page_count}
    header :
        None
'''
'''
    @post info
    method : POST
    url : 
        self.post_url + href
    header :
        None
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '신용보증기금'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.kodit.co.kr/kodit/na/ntt/selectNttInfo.do?searchType=all&bbsId=148&nttSn={}&mi=2638'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
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