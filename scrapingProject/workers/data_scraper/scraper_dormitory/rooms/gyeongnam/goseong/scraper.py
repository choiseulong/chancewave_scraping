from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 고성군청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.geochang.go.kr/news/board/List.do?gcode=1002&pageCd=NW0101000000&siteGubun=portal&cpage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.geochang.go.kr/news/board/View.do?gcode=1002&idx={postId}&pageCd=NW0101000000&siteGubun=portal
    header :
        None

'''
sleep_sec = 1
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '고성군청'
        self.post_board_name = '보도자료'
        self.channel_main_url = 'https://www.goseong.go.kr'
        self.post_url = 'https://www.goseong.go.kr/board/view.goseong?boardId=BBS_0000070&menuCd=DOM_000000104001001001&startPage=1&dataSid={}'
        
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