from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://namgu.gwangju.kr/board.es?mid=a70501000000&bid=0261&nPage={}
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
    base64
'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '광주남구청'
        self.post_board_name = '장학회소식/공지사항'