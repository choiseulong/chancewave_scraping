from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 미추홀구복지포털

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.michuhol.go.kr/welfare/board/list.do?page={}&board_code=board_101
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
        self.channel_name = '미추홀구복지포털'
        self.post_board_name = '복지소식'
        self.post_url = 'https://www.michuhol.go.kr/welfare/board/'