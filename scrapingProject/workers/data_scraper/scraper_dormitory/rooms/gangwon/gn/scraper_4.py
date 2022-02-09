from .scraper_3 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.gn.go.kr/www/selectBbsNttList.do?key=3008&bbsNo=131&pageUnit=10&searchCnd=all&pageIndex={}
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
        self.channel_name = '강릉시청'
        self.post_board_name = '주민자치센터강좌'