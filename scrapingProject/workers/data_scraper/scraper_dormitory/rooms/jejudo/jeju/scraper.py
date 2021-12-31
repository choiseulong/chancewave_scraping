from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 제주

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시


#HTTP Request
'''
    @post list

    method : GET
    url = https://www.jeju.go.kr/news/news/news.htm?page={page_count}
    header :
        User-Agent
    required data searching point :
        header_1 : fixed
'''
'''
    @post info
    method : GET
    url : post_url
    header :
        None
'''

sleep_sec = 4
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '제주특별자치도'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.jeju.go.kr'
        
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
            
            if self.page_count == 4 :
                break
            
 
    def post_list_scraping(self):
        postBoardNameInfo = {
            'jeju_1' : '일자리/중소기업 알림마당',
            'jeju_2' : '일자리지원정책 알림마당',
            'jeju_3' : '평생교육강좌(민간)',
            'jeju_4' : '여성교육정보(민간)',
            'jeju_5' : '문화역사 알림마당'

        }
        if self.channel_code in postBoardNameInfo.keys():
            self.post_board_name = postBoardNameInfo[self.channel_code]
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)


            

 



