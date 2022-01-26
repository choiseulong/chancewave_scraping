from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url = https://www.namdong.go.kr/job/bbs/bbsMsgList.do?bcd=job_notice&pgno={}
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
        self.channel_name = '인천남동구청일자리센터'
        self.post_board_name = '공지사항'