from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 칠곡군청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.cheongdo.go.kr/open.content/ko/administration/news/notice/?p={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.usc.go.kr/board/detail.tc?mn=1275&viewType=sub&mngNo=275&pageIndex=1&boardName=EOVYRHDWL&boardNo={posrId}&pageSeq=1314
    header :
        None

'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '칠곡군청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.cheongdo.go.kr'
        self.post_url = 'https://www.chilgok.go.kr/portal/bbs/view.do?mId=0201010000&bIdx={}&ptIdx=111'
        
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