from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 부산강서구청

#HTTP Request
'''
    @post list
    method : GET
    url_0 =  https://www.bsgangseo.go.kr/bsgangseo/bbs/list.do?bsgsIdx=21&mId=0401010000&page={page_count}\
        &backUrl=/bsgangseo/bbs/write.do&backResetUrl=/bsgangseo/bbs/list.do
    header :
        None

'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id)
    header :
        None

'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산강서구청'
        self.post_board_name = '알림사항'
        self.post_url = 'https://www.bsgangseo.go.kr/bsgangseo/bbs/view.do?bIdx={}&bsgsIdx=21&mId=0401010000'

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