from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경상남도

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.gyeongnam.go.kr/board/list.gyeong?boardId=BBS_0000057&menuCd=DOM_000000104001001000&paging=ok&startPage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gyeongnam.go.kr/board/view.gyeong?boardId=BBS_0000057&menuCd=DOM_000000104001001000&paging=ok&dataSid={postId}
    header :
        None

'''
sleep_sec = 1
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '경상남도청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.gyeongnam.go.kr'
        self.post_url = 'https://www.gyeongnam.go.kr/board/view.gyeong?boardId=BBS_0000057&menuCd=DOM_000000104001001000&paging=ok&dataSid={}'
        
    def scraping_process(self, channel_code, channel_url):
        super().scraping_process(channel_code, channel_url)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True :
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()
            if self.scraping_target :
                if self.channel_code != 'gyeongnamdo_1':
                    self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else :
                break

    def post_list_scraping(self):
        parsingProcess = post_list_parsing_process
        if self.channel_code == 'gyeongnamdo_1':
            self.post_board_name = '팝업존'
            parsingProcess = postListParsingProcess_1
        super().post_list_scraping(parsingProcess, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)