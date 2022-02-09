from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = 페이지에서 찾은 url..
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
        self.channel_name = '동해시청'
        self.post_board_name = '문화예술행사'
        self.board_href_list = []
        self.board_title_list = []