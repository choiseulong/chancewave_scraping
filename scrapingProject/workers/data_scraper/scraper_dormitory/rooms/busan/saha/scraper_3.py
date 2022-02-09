from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.saha.go.kr/tour/bbs/list.do?ptIdx=61&mId=0201000000&page={}\
        &backUrl=/tour/bbs/write.do?ptIdx=61&backResetUrl=/tour/bbs/list.do?ptIdx=61&searchType=b_title
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
        self.channel_name = '부산사하구청'
        self.post_board_name = '행사안내'
        self.post_url = 'http://www.saha.go.kr/tour/bbs/view.do?bIdx={}&ptIdx={}&mId={}'