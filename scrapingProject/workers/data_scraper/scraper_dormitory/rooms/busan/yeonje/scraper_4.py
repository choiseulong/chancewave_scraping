from .scraper_3 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =  https://www.yeonje.go.kr/welfare/bbs/list.do?ptIdx=65&mId=0101000000&\
        cancelUrl=%%2Fwelfare%%2Fbbs%%2Flist.do%%3FptIdx%%3D65%%26mId%%3D0101000000&page={}
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산연제구복지포털'
        self.post_board_name = '알림사항'
        self.post_url = 'https://www.yeonje.go.kr/welfare/bbs/view.do?bIdx={}&ptIdx={}&mId={}'