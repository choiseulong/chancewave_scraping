from .scraper import Scraper as default_scraper

'''
    @post list
    method : GET
    url_0 = https://www.hsg.go.kr/life/health/00001077.web?gcode=1001&cpage={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url + href
    header :
        None
'''

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '횡성군청'
        self.post_board_name = '보건/건강/공지사항'
        self.post_url = 'https://www.hsg.go.kr/life/health/00001077.web'