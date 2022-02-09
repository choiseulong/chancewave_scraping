from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_1 import *

# 채널 이름 : 인제군청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = http://lifelong.inje.go.kr/brd/post/notice/list
    에서 리스트 탐색
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.channel_main_url + href
    header :
        None
'''
sleep_sec = 1
real_channel_url = 'http://lifelong.inje.go.kr/brd/post/notice/list?__encrypted={}&page.page={}&keyField=TITLE&searchWord='

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '인제군평생학습센터'
        self.post_board_name = '공지사항'

    def search_encrypted_value(self, channel_url):
        _, response = get_method_response(self.session, channel_url, sleep_sec)
        soup = change_to_soup(response.text)
        input_encrypted = extract_children_tag(soup, 'input', child_tag_attrs={'name':'__encrypted'})
        encrypted_value = extract_attrs(input_encrypted, 'value')
        channel_url = real_channel_url.replace('{}', encrypted_value, 1)
        return channel_url

    def scraping_process(self, channel_code, channel_url, dev):
        self.session = set_headers(self.session)
        channel_url = self.search_encrypted_value(channel_url)
        super().scraping_process(channel_code, channel_url, dev)
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