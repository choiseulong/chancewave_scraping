from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 대구광역시청

#HTTP Request
'''
    @post list
    method : GET
    url_0 =   https://www.daegu.go.kr/index.do?menu_id=00000854&menu_link=/icms/bbs/selectBoardList.do\
        &bbsId=BBS_00029&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&nttId=0&pageIndex={page_count}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url + post_id
    header :
        None

'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '대구광역시청'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.daegu.go.kr/index.do?menu_id=00000854&menu_link=/icms/bbs/selectBoardArticle.do&bbsId=BBS_00029&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&nttId='

    def scraping_process(self, channel_code, channel_url):
        super().scraping_process(channel_code, channel_url)
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