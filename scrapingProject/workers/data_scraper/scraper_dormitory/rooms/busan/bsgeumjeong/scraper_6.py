from .scraper_4 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://library.geumjeong.go.kr/board/list.geumj?boardId=BBS_0000131&menuCd=DOM_000000613001000000&startPage={}
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
        self.channel_name = '부산금정구보건소'
        self.post_board_name = '공지사항'