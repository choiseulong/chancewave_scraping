from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.djjunggu.go.kr/bbs/BBSMSTR_000000000063/list.do?pageIndex={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id) +
    header :
        None
'''
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '대전중구청'
        self.post_board_name = '커뮤니티/공지사항'
        self.post_url = 'https://www.djjunggu.go.kr/bbs/BBSMSTR_000000000063/view.do?nttId={}'