from .scraper_3 import Scraper as default_scraper
'''
    @post list
    method : GET
    url = https://www.inje.go.kr/health/participation/notice?pageIndex={}
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
        self.channel_name = '인제군보건소'
        self.post_board_name = '공지사항'