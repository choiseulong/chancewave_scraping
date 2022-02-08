from .scraper import Scraper as default_scraper

# 채널 이름 : 속초시청

#HTTP Request
'''
    @post list
    method : GET
    url = https://www.sokcho.go.kr/portal/happysokcho/businessplace/healthcenter/health_notice?pageIndex={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.channle_main_url + href
    header :
        None
'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '속초시보건소'
        self.post_board_name = '공지사항'