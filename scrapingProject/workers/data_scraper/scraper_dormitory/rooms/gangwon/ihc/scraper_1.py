from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.ihc.go.kr/www/selectBbsNttList.do?key=182&bbsNo=48&pageUnit=10&searchCnd=all&pageIndex={}
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
        self.channel_name = '화천군청'
        self.post_board_name = '교육/취업/공지사항'
        self.post_url = 'https://www.ihc.go.kr/www'