from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://bukgu.gwangju.kr/board.es?mid=a10201110000&bid=0315&nPage={}
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
        self.channel_name = '광주북구청'
        self.post_board_name = '문화행사'