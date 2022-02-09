from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.saha.go.kr/dadaelib/bbs/list.do?ptIdx=660&mId=0509000000page={}&\
        backUrl=/dadaelib/bbs/write.do?ptIdx=660&backResetUrl=/dadaelib/bbs/list.do?ptIdx=660&searchType=b_title
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format()
    header :
        None

'''
'''
    base64
'''
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산사하구다대도서관'
        self.post_board_name = '공지사항'
        self.post_url = 'http://www.saha.go.kr/dadaelib/bbs/view.do?bIdx={}&ptIdx={}&mId={}'