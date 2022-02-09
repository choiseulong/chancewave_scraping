from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.donggu.kr/board.es?mid=a70601000000&bid=0027&nPage={}
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
        self.channel_name = '광주동구보건소'
        self.post_board_name = '공지사항'