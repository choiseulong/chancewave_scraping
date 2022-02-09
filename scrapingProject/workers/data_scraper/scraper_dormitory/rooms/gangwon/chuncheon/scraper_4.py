from .scraper_3 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://cityhall.chuncheon.go.kr/board/list.chuncheon?boardId=BBS_0000564&menuCd=DOM_000011707004000000&startPage={}
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
        self.channel_name = '춘천시보건소'
        self.post_board_name = '강좌/행사안내'