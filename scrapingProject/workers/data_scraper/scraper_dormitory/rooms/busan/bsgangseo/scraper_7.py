from .scraper_5 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.bsgangseo.go.kr/health/bbs/list.do?bsgsIdx=244&mId=0405000000&page={}

    header :
        None

'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id) 
    header :
        None

'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산강서구청'
        self.post_board_name = '문화관광소식'
        self.post_url = 'https://www.bsgangseo.go.kr/visit/bbs/view.do?bIdx={}&bsgsIdx=21&mId=06010000000'