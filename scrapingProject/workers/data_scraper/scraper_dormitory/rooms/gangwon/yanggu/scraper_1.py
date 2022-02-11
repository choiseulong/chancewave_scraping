from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser_1 import *
'''
    @post list
    method : GET
    url_0 =  https://www.yanggu.go.kr/lll/yglll/bbs_list.do?code=sub07a&keyvalue=sub07
    에서 찾음
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url + href
    header :
        None
'''
'''
    base64
'''
sleep_sec = 1

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '양구군청'
        self.post_board_name = '양구뉴스'
        self.post_url = 'https://www.yanggu.go.kr/lll/yglll/'
    
    def search_bbs_data(self, channel_url):
        self.channel_url_list = [channel_url]
        _, response = get_method_response(self.session, channel_url, sleep_sec)
        soup = change_to_soup(response.text)
        pagination_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'pagination'})
        pagination_list = extract_children_tag(pagination_box, 'a', child_tag_attrs={'href':True}, is_child_multiple=True)
        page_url_frame = 'https://www.yanggu.go.kr/lll/yglll/bbs_list.do?code=sub07a&keyvalue=sub07&'
        for a_tag in pagination_list:
            href = extract_attrs(a_tag, 'href')
            if 'bbs_data' in href:
                self.channel_url_list.append(
                    page_url_frame + href[1:]
                )

    def scraping_process(self, channel_code, channel_url, dev):
        self.session = set_headers(self.session)
        self.search_bbs_data(channel_url)
        self.page_count = 1
        for channel_url in self.channel_url_list:
            self.channel_url = channel_url
            super().scraping_process(channel_code, channel_url, dev)
            self.post_list_scraping()
            if self.scraping_target :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break

    def post_list_scraping(self):
        if self.page_count == 1:
            super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)
        else:
            super().post_list_scraping(post_list_parsing_process, 'urlopen', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)