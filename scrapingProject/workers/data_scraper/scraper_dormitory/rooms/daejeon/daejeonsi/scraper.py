from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 대전광역시청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.daejeon.go.kr/drh/board/boardNormalList.do?pageIndex={}&boardId=normal_0096&menuSeq=1631
    url_1 = https://www.daejeon.go.kr/fvu/FvuEventList.do?menuSeq=504&pageIndex={}
    
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
        self.channel_name = '대전광역시청'
        self.post_board_name = ''

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
        search_post_list = ''
        if self.channel_code == 'daejeonsi_0':
            self.post_board_name = '시정소식'
            search_post_list = post_list_parsing_process
        elif self.channel_code == 'daejeonsi_1':
            self.post_board_name = '행사안내'
            search_post_list = post_list_parsing_process_1

        super().post_list_scraping(search_post_list, 'get', sleep_sec)

    def target_contents_scraping(self):
        search_contents = ''
        if self.channel_code == 'daejeonsi_0':
            search_contents = post_content_parsing_process
        elif self.channel_code == 'daejeonsi_1':
            search_contents = post_content_parsing_process_1
        super().target_contents_scraping(search_contents, sleep_sec)