from .scraper import Scraper as default_scraper
from .parser import *

# 채널 이름 : 연수구청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.yeonsu.go.kr/clinic/participation/news.asp?gotopage={}
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
'''
    base64 포함
'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '연수구청보건소'
        self.post_board_name = '보건뉴스'