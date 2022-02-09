from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 미추홀구평생학습관

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.michuhol.go.kr/lll/board/list.do?page={}&board_code=l_board_1&srchCate=&srchKey=ABC&srchValue=
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
        self.channel_name = '미추홀구평생학습관'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.michuhol.go.kr/lll/board/'