from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 예산군청평생학습
#HTTP Request
'''
    @post list
    method : GET
    url_0 =   https://welfare.yesan.go.kr/cop/bbs/BBSMSTR_000000000581/selectBoardList.do?pageIndex={}
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
        self.channel_name = '예산군청평생학습'
        self.post_board_name = '공지사항'