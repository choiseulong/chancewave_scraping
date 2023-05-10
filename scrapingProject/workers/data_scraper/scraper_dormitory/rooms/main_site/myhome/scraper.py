from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 마이홈


# 타겟 : 모집중인 공고
# 중단 시점 : 모든 공고가 모집 완료인 시점에서 종료

#HTTP Request
'''
    @post list

    method : POST -> GET
    url = https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcList.do
    url = https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcList.do?pageIndex={page_count}&srchSuplyTy= 수정
    header :
        1. Content-Type : application/x-www-form-urlencoded; charset=UTF-8

        수정
        1. None
    body :
        1. pageIndex={page_count}
        2. srchSuplyTy=

        수정 
        미사용

    required data searching point :
        header_1 : fixed
        body_1 : page_count
        body_2 : fixed
'''
'''
    @post info

    method : get
    url : 'post_url'
    header :
        None
'''

is_update = True
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '마이홈'
        self.post_board_name = '입주자모집공고'
        self.post_url = "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId={}"

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True :
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()
            # self.response = self.session.get(self.channel_url)
            # self.scraping_target = post_list_parsing_process(
            #         response = self.response, 
            #         channel_code = self.channel_code, 
            #         post_url_frame = self.post_url,
            #         page_count = self.page_count,
            #         channel_main_url = self.channel_main_url,
            #         channel_url = self.channel_url,
            #         dev = self.dev,
            # )
            if self.scraping_target :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else:
                break

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        for target in self.scraping_target:
            post_url = target['post_url']
            response = self.session.get(post_url)
            post_content = post_content_parsing_process(
                response = response, 
                channel_url = self.channel_url,
                post_url_frame = self.post_url,
                channel_main_url = self.channel_main_url,
                channel_code = self.channel_code,
                dev = self.dev
            )
            self.scraping_target_contents.append(post_content)
    



            

 

