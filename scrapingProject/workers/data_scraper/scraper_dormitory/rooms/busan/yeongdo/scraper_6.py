from .scraper_4 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =   https://www.yeongdo.go.kr/tour/01526/01527.web?gcode=1160&cpage={}
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
        self.channel_name = '부산영동구문화관광'
        self.post_board_name = '관광소식'
        self.post_url = 'https://www.yeongdo.go.kr/tour/01526/01527.web'