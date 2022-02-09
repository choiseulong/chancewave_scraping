from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.gn.go.kr/www/selectBbsNttList.do?key=267&bbsNo=18&pageUnit=10&searchCnd=all&pageIndex={}
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '강릉시청'
        self.post_board_name = '타기관소식'