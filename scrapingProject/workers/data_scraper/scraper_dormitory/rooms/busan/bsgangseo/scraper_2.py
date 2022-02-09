from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 =  https://www.bsgangseo.go.kr/welfare/bbs/list.do?bIdx=158741&bsgsIdx=21&mId=0107000000&page={}
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
        self.channel_name = '부산강서구복지행정'
        self.post_board_name = '알림사항'
        self.post_url = 'https://www.bsgangseo.go.kr/welfare/bbs/view.do?bIdx={}&bsgsIdx=21&mId=0107000000'