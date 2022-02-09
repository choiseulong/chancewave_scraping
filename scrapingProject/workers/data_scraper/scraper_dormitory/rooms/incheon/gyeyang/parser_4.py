from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.gyeyang.go.kr/open_content/main/bbs/bbsMsgList.do?bcd=board_130&pgno={}
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
        self.channel_name = '계양구보건소'
        self.post_board_name = '공지사항'