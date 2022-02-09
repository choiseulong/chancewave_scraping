from .scraper_2 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =https://www.busanjin.go.kr/board/list.busanjin?boardId=BBS_0000224&menuCd=DOM_000000107008002000&paging=ok&startPage={}
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
        self.channel_name = '부산진구청'
        self.post_board_name = '복지 모아 알림방'