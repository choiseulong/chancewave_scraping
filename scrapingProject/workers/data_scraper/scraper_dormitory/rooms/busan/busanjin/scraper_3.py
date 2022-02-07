from .scraper_2 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.busanjin.go.kr/happy/board/list.busanjin?boardId=BBS_0000157&menuCd=DOM_000001904001000000&paging=ok&startPage={}
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
        self.channel_name = '부산진구다행복교육지원센터'
        self.post_board_name = '공지사항'