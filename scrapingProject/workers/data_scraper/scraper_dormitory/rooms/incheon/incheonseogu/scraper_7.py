from .scraper_3 import Scraper as default_scraper

# 채널 이름 : 인천서구청보건소

#HTTP Request
'''
    @post list
    method : GET
    url = https://www.seo.incheon.kr/open_content/clinic/bbs/bbsMsgList.do?bcd=health_news&pgno={}
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
sleep_sec = 1

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '인천서구청보건소'
        self.post_board_name = '보건소식'