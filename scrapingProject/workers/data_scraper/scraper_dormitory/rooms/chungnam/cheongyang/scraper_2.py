from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 청양군청평생학습센터
# HTTP Request
'''
    @post list
    method : GET
    url =  http://www.cheongyang.go.kr/cop/bbs/BBSMSTR_000000000146/selectBoardList.do?pageIndex={}
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

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '청양군청평생학습센터'
        self.post_board_name = '공지사항'