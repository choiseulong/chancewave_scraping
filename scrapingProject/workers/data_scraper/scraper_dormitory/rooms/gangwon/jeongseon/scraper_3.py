from .scraper_2 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.jeongseon.go.kr/tour/travelguide/travel_news?pageIndex={}
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
        self.channel_name = '정선군보건소'
        self.post_board_name = '공지사항'