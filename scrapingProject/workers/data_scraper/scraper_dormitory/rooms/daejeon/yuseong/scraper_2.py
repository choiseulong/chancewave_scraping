from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.yuseong.go.kr/bbs/BBSMSTR_000000000082/list.do?pageIndex={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url_frame(post_id)
    header :
        None
'''
'''
    pdf 포함
'''
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '유성구청보건소'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.yuseong.go.kr/bbs/BBSMSTR_000000000082/view.do?nttId={}'