from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 산림청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.forest.go.kr/kfsweb/cop/bbs/selectBoardList.do?mn=NKFS_04_01_01&pageIndex={}&pageUnit=50&searchtitle=title&bbsId=BBSMSTR_1031
    header :
        None

'''
'''
    @post info
    method : GET
    url : 'https://www.forest.go.kr/kfsweb/cop/bbs/selectBoardArticle.do?nttId={postId}&bbsId=BBSMSTR_1031&searchtitle=title&mn=NKFS_04_01_01'
    header :
        None

'''
sleep_sec = 4
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '산림청'
        self.post_board_name = '알림정보'
        self.channel_main_url = 'https://www.forest.go.kr'
        self.post_url = 'https://www.forest.go.kr/kfsweb/cop/bbs/selectBoardArticle.do?nttId={}&bbsId=BBSMSTR_1031&searchtitle=title&mn=NKFS_04_01_01'
        
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

    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)