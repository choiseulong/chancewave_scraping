from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 옹진군청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.ongjin.go.kr/open_content/main/bbs/bbsMsgList.do?bcd=report&pgno={}
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
        self.channel_name = '옹진군청'
        self.post_board_name = '보도/해명'
