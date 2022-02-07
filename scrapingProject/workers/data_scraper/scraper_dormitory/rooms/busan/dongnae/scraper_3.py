from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.dongnae.go.kr/lll/board/list.dongnae?boardId=BBS_0000122&listRow=10&listCel=1&menuCd=DOM_000000702001000000&startPage={}
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
        self.channel_name = '부산동래구평생학습관'
        self.post_board_name = '강좌안내'