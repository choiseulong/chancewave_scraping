from .scraper import Scraper as default_scrpaer
'''
    @post list
    method : GET
    url_0 =  https://www.yw.go.kr/www/selectBbsNttList.do?key=26&bbsNo=16&pageUnit=10&searchCnd=all&pageIndex={}
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
class Scraper(default_scrpaer):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '영월군청'
        self.post_board_name = '타기관소식'
        self.post_url = 'https://www.yw.go.kr/www'