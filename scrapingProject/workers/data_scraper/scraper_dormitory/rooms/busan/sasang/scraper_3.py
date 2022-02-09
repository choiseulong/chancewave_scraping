from .scraper_2 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.sasang.go.kr/board/list.sasang?boardId=BBS_0000080&menuCd=DOM_000000406001000000&startPage={}
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산사상보건소'
        self.post_board_name = '공지사항'