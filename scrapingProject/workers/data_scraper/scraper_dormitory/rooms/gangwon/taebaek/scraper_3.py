from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.taebaek.go.kr/health/selectBbsNttList.do?key=624&bbsNo=65&pageUnit=10&searchCnd=all&pageIndex={}
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
        self.channel_name = '태백시보건소'
        self.post_board_name = '공지사항'
        self.post_url = 'http://www.taebaek.go.kr/health'