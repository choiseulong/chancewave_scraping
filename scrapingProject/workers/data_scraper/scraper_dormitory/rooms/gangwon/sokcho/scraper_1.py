from .scraper import Scraper as default_scraper

# 채널 이름 : 속초시청

#HTTP Request
'''
    @post list
    method : GET
    url_0 = https://www.sokcho.go.kr/portal/openinfo/sokchonews/edu_culture?pageIndex={}
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
        self.channel_name = '속초시청'
        self.post_board_name = '교육/문화'