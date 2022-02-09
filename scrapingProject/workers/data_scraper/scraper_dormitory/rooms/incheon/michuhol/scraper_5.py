from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 미추홀구보건소

#HTTP Request
'''
    @post list
    method : GET
    url = https://www.michuhol.go.kr/clinic/board/list.do?board_code=board_1&\
        site_code=clinic&dept_search_query_data=allClinic&page={}&srchCate=&srchKey=AB&srchValue=
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '미추홀구보건소'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.michuhol.go.kr/clinic/board/'