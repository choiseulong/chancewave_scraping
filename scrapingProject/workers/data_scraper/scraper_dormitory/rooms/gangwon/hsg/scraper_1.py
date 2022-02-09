from .scraper import Scraper as default_scraper

'''
    @post list
    method : GET
    url_0 = https://www.hsg.go.kr/life/00000590/00000884.web?gcode=2042&cpage={}
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
        self.post_board_name = '교육새소식'
        self.post_url = 'https://www.hsg.go.kr/life/00000590/00000884.web'