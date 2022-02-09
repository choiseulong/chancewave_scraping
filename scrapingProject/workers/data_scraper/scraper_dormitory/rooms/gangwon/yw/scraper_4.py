from .scraper_2 import Scraper as default_scraper

'''
    @post list
    method : GET
    url_0 =   https://www.yw.go.kr/www/selectBbsNttList.do?key=397&bbsNo=37&pageUnit=10&searchCnd=all&pageIndex={}
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
        self.channel_name = '영월여성새로일하기센터'
        self.post_board_name = '공지사항'
        self.post_url = 'https://www.yw.go.kr/www'