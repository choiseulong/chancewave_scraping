import imp
from .scraper import Scraper as default_scraper

# 채널 이름 : 철원군청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.cwg.go.kr/www/selectBbsNttList.do?key=206&bbsNo=24&searchCnd=all&pageIndex={}
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
        self.channel_name = '철원군청'
        self.post_board_name = '고시/공고'
        self.post_url = 'https://www.cwg.go.kr/www'