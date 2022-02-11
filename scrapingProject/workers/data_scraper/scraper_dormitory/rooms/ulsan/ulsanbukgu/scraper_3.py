from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_3 import *

# 채널 이름 : 울산북구평생학습관

#HTTP Request
'''
    @post list
    method : GET
    url =  https://www.bukgu.ulsan.kr/edu/join/join1.jsp?pagenum={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : self.channel_main_url + href
    header :
        None

'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '울산북구평생학습관'
        self.post_board_name = '평생학습강좌'
        self.post_url = 'https://crs.ubimc.or.kr/lecture/step1?lecId={}'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        print(channel_code, full_channel_code)
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.additional_key_value.append(("Referer", f"https://www.bukgu.ulsan.kr/edu/pageCont.do?pageIndex=1&menuNo=2010000"))
        self.session = set_headers(self.session, self.additional_key_value, is_update)
        self.channel_url = self.channel_url_frame
        self.post_list_scraping()
        if self.scraping_target :
            self.target_contents_scraping()
            self.collect_data()
            self.mongo.reflect_scraped_data(self.collected_data_list)

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)