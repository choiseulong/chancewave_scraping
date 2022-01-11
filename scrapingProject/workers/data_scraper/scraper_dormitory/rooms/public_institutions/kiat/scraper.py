from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 한국산업기술진흥원

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.kiat.or.kr/front/board/boardContentsListAjax.do?miv_pageNo={page_count}\
        &mode=W&board_id=5&MenuId=2124728cc8cc4b74a31bbe97d7977c6d&state_filter=W
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id)
    header :
        None
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '한국산업기술진흥원'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.kiat.or.kr/front/board/boardContentsView.do?mode=W&contents_id={}&board_id=5&intropage_boardUseYn=&MenuId=2124728cc8cc4b74a31bbe97d7977c6d'

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