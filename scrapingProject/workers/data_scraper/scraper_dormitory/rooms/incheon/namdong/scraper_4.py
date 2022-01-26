from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url = https://www.namdong.go.kr/clinic/bbs/bbsMsgList.do?bcd=clinic_news&pgno={}
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
        self.channel_name = '인천남동구보건소'
        self.post_board_name = '보건소소식'