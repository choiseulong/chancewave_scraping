from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 보건복지부

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  http://www.mohw.go.kr/react/al/sal0101ls.jsp?PAR_MENU_ID=04&MENU_ID=040101&page={page_count} 
    header :
        1.Content-Type: application/x-www-form-urlencoded
    body :
        None
    required data searching point :
        None

'''
'''
    @post info
    method : GET
    url : http://www.mohw.go.kr/react/al/sal0101vw.jsp?PAR_MENU_ID=04&MENU_ID=040101&CONT_SEQ={postId}
    header :
        None

'''
sleep_sec = 1
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '보건복지부'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'http://www.mohw.go.kr'
        self.post_url = 'http://www.mohw.go.kr/react/al/sal0101vw.jsp?PAR_MENU_ID=04&MENU_ID=040101&CONT_SEQ={}'
        
    def scraping_process(self, channel_code, channel_url):
        super().scraping_process(channel_code, channel_url)
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