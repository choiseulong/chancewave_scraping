from .scraper_4 import Scraper as default_scraper
'''
    @post list
    method : GET
    url =   https://www.yeongdo.go.kr/02418/02419/02576.web?cpage={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url + href
    header :
        None

'''

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부산영동구복지넷'
        self.post_board_name = '복지행사'
        self.post_url = 'https://www.yeongdo.go.kr/02418/02419/02576.web'