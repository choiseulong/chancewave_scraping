from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.jeongseon.go.kr/portal/openadmin/adminnews/othernews?pageIndex={}
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
        self.channel_name = '정선군청'
        self.post_board_name = '타기관소식'