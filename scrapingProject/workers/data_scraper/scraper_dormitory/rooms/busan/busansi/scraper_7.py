from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 =  https://www.busan.go.kr/depart/pbnews?curPage={}
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
        self.channel_name = '부산광역시청'
        self.post_board_name = '문화체육관광/공지사항'