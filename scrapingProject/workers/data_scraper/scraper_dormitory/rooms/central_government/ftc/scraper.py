from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 공정거래위원회

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.ftc.go.kr/www/cop/bbs/selectBoardList.do?key=13
    header :
        1. Content-Type: application/x-www-form-urlencoded
    body : 
        1. bbsId=BBSMSTR_000000002424
        2. bbsTyCode=BBST01
        3. pageIndex=1

    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : fixed
        body_3 : page_count

'''
'''
    @post info
    method : POST
    url : https://www.ftc.go.kr/www/cop/bbs/selectBoardArticle.do?key=13
    header :
        None
    body : 
        data = {
            "bbsId" : "BBSMSTR_000000002424",
            "bbsTyCode" : "BBST01",
            "nttId" : {nttId},
            "pageIndex" : self.page_count
        }
    required data searching point :
        header_1 : fixed
        body_1 = {nttId}
'''

sleep_sec = 4
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '공정거래위원회'
        self.post_board_name = '공지/공고'
        self.channel_main_url = 'https://www.ftc.go.kr'
        self.post_url = 'https://www.ftc.go.kr/www/cop/bbs/selectBoardArticle.do?key=13'
        
    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)

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
            "bbsId" : "BBSMSTR_000000002424",
            "bbsTyCode" : "BBST01",
            "nttId" : 0,
            "pageIndex" : self.page_count
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)


            

 



