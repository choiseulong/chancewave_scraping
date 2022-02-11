from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 원자력안전위원회

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.nssc.go.kr/ajaxf/FR_BBS_SVC/BBSViewList.do
    header :
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. pageNo = {page_count}
        2. pagePerCnt = 15
        3. MENU_ID = 180
        4. SITE_NO = 2
        5. BOARD_SEQ = 4

    required data searching point :
        header_1 : fixed
        body_1 : {page_count}
        body_other : fixed

'''
'''
    @post info
    method : POST
    url : https://www.nssc.go.kr/ajaxf/FR_BBS_SVC/BoardViewData.do
    header :
        None
    body : 
        data = {
            "MENU_ID" : 180,
            "SITE_NO" : 2,
            "BOARD_SEQ" : 4, 
            "BBS_SEQ" : {postId}
        }
    required data searching point :
        header_1 : fixed
        body_1 = {nttId}
'''

sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '원자력안전위원회'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.nssc.go.kr'
        self.post_url = 'https://www.nssc.go.kr/ajaxf/FR_BBS_SVC/BoardViewData.do?MENU_ID=180&SITE_NO=2&BOARD_SEQ=4&BBS_SEQ={}&CONTENTS_NO=1'
        
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


            

 



