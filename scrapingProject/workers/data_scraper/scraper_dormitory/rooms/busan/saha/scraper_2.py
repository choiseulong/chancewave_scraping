from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  http://www.saha.go.kr/edu/bbs/list.do?ptIdx=115&mId=0501000000&page={}\
        &backUrl=/edu/bbs?write.do?ptIdx=115&backResetUrl=/edu/bbs/list.do?ptIdx=115&searchType=b_title
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
        self.channel_name = '부산사하구평생학습관'
        self.post_board_name = '공지사항'
        self.post_url = 'http://www.saha.go.kr/edu/bbs/view.do?bIdx={}&ptIdx={}&mId={}'