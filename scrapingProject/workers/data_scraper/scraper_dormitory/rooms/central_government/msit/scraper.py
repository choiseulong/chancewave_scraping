from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 과학기술정보통신부

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.msit.go.kr/bbs/list.do?sCode=user&mId=129&mPid=128&pageIndex={page_count}
    url = https://www.msit.go.kr/bbs/list.do?sCode=user&mId=129&mPid=224&pageIndex={page_count}&bbsSeqNo=100
    header :
        None
'''
'''
    @post info
    method : GET
    url : https://www.msit.go.kr/bbs/view.do?sCode=user&mId=129&mPid=128&bbsSeqNo=100&nttSeqNo={postId}
    header :
        None

'''

sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '과학기술정보통신부'
        self.post_board_name = '사업공고'
        self.channel_main_url = 'https://www.msit.go.kr'
        # self.post_url = 'https://www.msit.go.kr/bbs/view.do?sCode=user&mId=129&mPid=128&bbsSeqNo=100&nttSeqNo={}'
        self.post_url = 'https://www.msit.go.kr/bbs/view.do?sCode=user&mId=129&mPid=224&bbsSeqNo=100&nttSeqNo={}'

        
    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
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