from .scraper import Scraper as default_scraper

'''
    @post list
    method : GET
    url = https://www.seogu.gwangju.kr/board.es?mid=a10311010700&bid=0037&nPage={}
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
        self.channel_name = '광주서구청'
        self.post_board_name = '타기관소식'