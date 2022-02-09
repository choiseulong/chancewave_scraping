from .scraper import Scraper as default_scraper

# 채널 이름 : 평창군청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.pc.go.kr/portal/government/government-news/government-news-otheragency?pageIndex={}
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
'''
    base64
'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '평창군청'
        self.post_board_name = '타기관소식'
