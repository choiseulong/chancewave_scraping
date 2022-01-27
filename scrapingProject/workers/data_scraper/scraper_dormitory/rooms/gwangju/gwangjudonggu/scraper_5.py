from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.donggu.kr/board.es?mid=a60701000000&bid=0019&nPage={}
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
        self.channel_name = '광주동구평생학습도시'
        self.post_board_name = '공지사항'