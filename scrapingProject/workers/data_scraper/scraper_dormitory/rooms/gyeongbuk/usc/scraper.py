from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 의성군청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.usc.go.kr/board/list.tc?mn=1275&viewType=sub&mngNo=275&pageIndex={page_count}&boardName=EOVYRHDWL&boardNo=0&pageSeq=1314
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
        self.channel_name = '의성군청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.usc.go.kr'
        self.post_url = 'https://www.usc.go.kr/board/detail.tc?mn=1275&viewType=sub&mngNo=275&pageIndex=1&boardName=EOVYRHDWL&boardNo={}&pageSeq=1314'
        
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