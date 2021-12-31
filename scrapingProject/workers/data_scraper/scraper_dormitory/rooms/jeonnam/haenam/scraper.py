from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 해남군청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = http://www.haenam.go.kr/planweb/board/list.9is?nowPageNum={page_count}\
        &boardUid=18e3368f5fb80fdc015fdc42b7e003e0&layoutUid=&contentUid=18e3368f5d745106015d877ab2850a94
    header :
        None

'''
'''
    @post info
    method : GET
    url : self.post_url + href[1:]
    header :
        None

'''
sleep_sec = 4
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '해남군청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'http://www.haenam.go.kr'
        self.post_url = 'http://www.haenam.go.kr/planweb/board'
        
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