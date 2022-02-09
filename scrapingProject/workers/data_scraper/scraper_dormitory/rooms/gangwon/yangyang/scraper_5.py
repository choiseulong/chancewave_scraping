from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.yangyang.go.kr/gw/healthcenter/healthnews_healthnotice?mode=listForm&boardCode=TBDDDEE01&curPage={}
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
        self.channel_name = '양양군보건소'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.yangyang.go.kr/gw/healthcenter/healthnews_healthnotice?mode=readForm&boardCode=TBDDDEE01&articleSeq={}'