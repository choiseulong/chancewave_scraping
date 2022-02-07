from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url = https://www.yeongdo.go.kr/00000/00007/00009.web?gcode=1026&cpage={}
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산영동구청'
        self.post_board_name = '행사/교육'
        self.post_url = 'https://www.yeongdo.go.kr/00000/00007/00009.web'