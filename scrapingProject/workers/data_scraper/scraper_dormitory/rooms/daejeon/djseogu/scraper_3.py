from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url = https://www.seogu.go.kr/sorg/board.do?mnucd=SGMENU0800093&pageIndex={}
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
        self.channel_name = '대전서구보건소'
        self.post_board_name = '공지사항'