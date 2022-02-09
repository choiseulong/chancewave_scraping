from .scraper_2 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.gwangju.go.kr/boardList.do?pageId=www955&movePage={}\
        &searchCtgry=25&boardId=BD_0305190100&searchTy=TM
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '광주김치타운관리사무소'
        self.post_board_name = '새소식'