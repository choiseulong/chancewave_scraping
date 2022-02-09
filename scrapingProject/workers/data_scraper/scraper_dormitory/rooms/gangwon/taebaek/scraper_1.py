from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = http://www.taebaek.go.kr/www/selectBbsNttList.do?key=352&bbsNo=25&pageUnit=10&searchCnd=all&pageIndex={}
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
        self.channel_name = '태백시청'
        self.post_board_name = '공고/고시'
        self.post_url = 'http://www.taebaek.go.kr/www'