from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 예산군청

#HTTP Request
'''
    @post list
    method : GET
    url_0 =   https://www.yesan.go.kr/cop/bbs/BBSMSTR_000000000064/selectBoardList.do?pageIndex={}
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

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.post_board_name = '타기관소식'