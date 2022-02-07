from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.saha.go.kr/health/bbs/list.do?ptIdx=44&mId=0102010000&page={}&\
        backUrl=/health/bbs?write.do?ptIdx=44&backResetUrl=/health/bbs/list.do?ptIdx=44&searchType=b_title
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
        self.channel_name = '부산사하구보건소'
        self.post_board_name = '공지사항'
        self.post_url = 'http://www.saha.go.kr/health/bbs/view.do?bIdx={}&ptIdx={}&mId={}'