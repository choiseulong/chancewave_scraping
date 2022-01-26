from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.icdonggu.go.kr/open_content/bbs.do?act=list&bcd=news&pageno={}
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
        self.channel_name = '인천동구청'
        self.post_board_name = '보도자료'