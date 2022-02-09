from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.dongnae.go.kr/board/list.dongnae?boardId=BBS_0000127&listRow=10&listCel=1&menuCd=DOM_000000507000000000&startPage={}
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
        self.channel_name = '부산동래복지정보'
        self.post_board_name = '알림/공지'