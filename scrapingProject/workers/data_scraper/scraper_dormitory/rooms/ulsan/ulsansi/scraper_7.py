from .scraper_2 import Scraper as parents_scraper
from .parser_2 import *


# 채널 이름 : 울산광역시청

#HTTP Request
'''
    @post list
    method : GET
    url_0 =  https://www.ulsan.go.kr/u/envi/bbs/list.ulsan?\
        bbsId=BBS_0000000000000067&mId=001001000000000000&page={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : self.post_url + href
    header :
        None

'''
class Scraper(parents_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '울산광역시청'
        self.post_board_name = '환경/새소식'
        self.post_url = 'https://www.ulsan.go.kr/u/envi/bbs'