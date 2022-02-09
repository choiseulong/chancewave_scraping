from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.pc.go.kr/health/community/community-notice?pageIndex={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.channel_main_url + href
    header :
        None
'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '평창군청'
        self.post_board_name = '공연안내'
