from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기콘텐츠진흥원

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시


#HTTP Request
'''
    @post list

    method : GET
    url = https://www.gcon.or.kr/busiNotice?pageNum={page_count}&rowCnt={포스트 숫자}&menuId=MENU02369
    header :
        User-Agent
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : https://www.gcon.or.kr/busiNotice/view?pageNum=1&rowCnt=10&linkId={linkId}&menuId=MENU02369
    header :
        User-Agent
    required data searching point :
        header_1 : fixed
'''

sleep_sec = 4

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '경기콘텐츠진흥원'
        self.post_board_name = '사업공고'
        self.channel_main_url = "https://www.gcon.or.kr"
    
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
        parsingFunc = post_content_parsing_process
        if '1' in self.channel_code:
            parsingFunc = postContentParsingProcess_other
            self.post_board_name = '교육 및 행사'
        super().target_contents_scraping(parsingFunc, sleep_sec)