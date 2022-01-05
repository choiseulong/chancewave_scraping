from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 세종시

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.sejong.go.kr/bbs/R0071/list.do
    header :
        Accept-Encoding: gzip, deflate, br
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : post_url
    header :
        Accept-Encoding: gzip, deflate, br
    required data searching point :
        header_1 : fixed
'''

sleep_sec = 1
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '세종시청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.sejong.go.kr'
    
    def scraping_process(self, channel_code, channel_url):
        super().scraping_process(channel_code, channel_url)
        self.additional_key_value.append(['Accept-Encoding', 'gzip, deflate, br'])
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)
        self.page_count = 1
        while True :
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
            "pageIndex" : self.page_count
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)


            

 



