from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 =   https://www.bsbukgu.go.kr/edu/board/list.bsbukgu?boardId=BBS_0000068&\
        menuCd=DOM_000000606001000000&paging=ok&startPage={}
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
        self.channel_name = '부산북구평생학습관'
        self.post_board_name = '공지사항'