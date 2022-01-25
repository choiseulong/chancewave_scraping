from .parser import *
from .scraper import Scraper as default_scraper

# 채널 이름 : 서천군보건소

#HTTP Request
'''
    @post list
    method : GET
    url =  http://www.seocheon.go.kr/cop/bbs/BBSMSTR_000000000105/selectBoardList.do?pageIndex={}
    header :
        None

'''
'''
    @post info5
    method : GET
    url : 
        self.channel_main_url + href
    header :
        None

'''

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '서천군보건소'
        self.post_board_name = '공지사항'