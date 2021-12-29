from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기도청

# 타겟 : 분야별 소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.gg.go.kr/bbs/board.do?bsIdx=570&menuId=1590#page={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gg.go.kr/bbs/boardView.do?bIdx={postId}&bsIdx=570&bcIdx=0&menuId=1590&isManager=false&isCharge=false&page=1
    header :
        None

'''
sleepSec = 2
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '경기도청'
        self.post_board_name = '분야별 소식'
        self.channel_main_url = 'https://www.gg.go.kr/'
        self.post_url = 'https://www.gg.go.kr/bbs/boardView.do?bIdx={}&bsIdx=570&bcIdx=0&menuId=1590&isManager=false&isCharge=false&page=1'

    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        self.session = set_headers(self.session)
        self.page_count = 0
        while True:
            self.channel_url = self.channel_url_frame.format(self.page_count)
            list_param = {
                'bsIdx': 570,
                'bcIdx': 0,
                'menuId': 1590,
                'isManager': 'false',
                'isCharge': 'false',
                'offset': self.page_count * 10,
                'limit': 10
            }

            self.channel_url = 'https://www.gg.go.kr/ajax/board/getList.do'

            self.post_list_scraping(post_list_parsing_process, 'post', data=list_param, jsonize=False)
            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else:
                break

    # def post_list_scraping(self):
    ## post 방식이라면 super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)
    #     super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)