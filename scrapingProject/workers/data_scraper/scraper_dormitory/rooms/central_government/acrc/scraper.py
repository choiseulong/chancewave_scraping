from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 국민권익위원회

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url = https://www.acrc.go.kr/acrc/board.do?command=searchDetail&menuId=05050101&currPageNo={page_count}
    수정 url : https://www.acrc.go.kr/board.es?mid=a10401010000&bid=2A&nPage={}
    header :
        None

'''
'''
    @post info
    
    method : GET
    url : post_url
'''

sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '국민권익위원회'
        # self.post_board_name = '공지사항' # 이전 게시판 이름
        self.post_board_name = '알립니다'

        self.channel_main_url = 'https://www.acrc.go.kr'
        
    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True :
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()
            if self.scraping_target :
                self.target_contents_scraping()
                # self.collect_data()
                # self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break

            if self.page_count == 3 :
                break

    def post_list_scraping(self):
        # data = {
        #     "bbsId" : "BBSMSTR_000000002424",
        #     "bbsTyCode" : "BBST01",
        #     "nttId" : 0,
        #     "pageIndex" : self.page_count
        # }
        # super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)
        super().post_list_scraping(post_list_parsing_process, 'get')

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)


            

 



