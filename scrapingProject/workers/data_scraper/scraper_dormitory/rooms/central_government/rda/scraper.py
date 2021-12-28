from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 농촌진흥청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.rda.go.kr/board/board.do?prgId=nei_ancmttEntry&currPage={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.rda.go.kr/board/board.do?boardId=ancmtt&prgId=nei_ancmttEntry&dataNo={postId}
    header :
        None

'''
sleep_sec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '농촌진흥청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.rda.go.kr'
        self.post_url = 'https://www.rda.go.kr/board/board.do?boardId=ancmtt&prgId=nei_ancmttEntry&menu_id=pun&currPage=1&dataNo={}&mode=updateCnt'
        
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
        data = {
            "page" : self.page_count,
            "row" : 50
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)