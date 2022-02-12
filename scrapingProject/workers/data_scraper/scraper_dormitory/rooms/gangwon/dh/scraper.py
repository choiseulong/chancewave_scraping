from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 동해시청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = 페이지에서 찾은 url..
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

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '동해시청'
        self.post_board_name = '공지사항'
        self.board_href_list = []
        self.board_title_list = []
    
    def search_board_href_list(self, channel_url):
        _, response = get_method_response(self.session, channel_url)
        soup = change_to_soup(response.text)
        paging_list = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'paging'})
        a_list = extract_children_tag(paging_list, 'a', is_child_multiple=True)
        self.board_title_list = [extract_attrs(a_tag, 'title') for a_tag in a_list]
        self.board_href_list = [extract_attrs(a_tag, 'href') for a_tag in a_list]
    
    def refresh_board_list_box_url(self):
        for title_idx, title in enumerate(self.board_title_list):
            if '다음 10페이지' == title:
                board_list_box_url = self.channel_main_url + self.board_href_list[title_idx]
                return board_list_box_url

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        board_list_box_url = channel_url
        while True:
            self.search_board_href_list(board_list_box_url)
            for href_idx, href in enumerate(self.board_href_list) :
                try :
                    self.page_count = int(self.board_title_list[href_idx].split(' ')[0])
                except ValueError:
                    continue
                self.channel_url = self.channel_main_url + href
                self.post_list_scraping()
                if self.scraping_target :
                    self.target_contents_scraping()
                    self.collect_data()
                    self.mongo.reflect_scraped_data(self.collected_data_list)
                else :
                    break
            if not self.scraping_target :
                break
            board_list_box_url = self.refresh_board_list_box_url()

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)