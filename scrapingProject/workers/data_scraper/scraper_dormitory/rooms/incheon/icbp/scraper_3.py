from .scraper import Scraper as default_scraper


# 채널 이름 : 부평구청

#HTTP Request
'''
    @post list
    method : GET
    url = https://www.icbp.go.kr/main/bbs/bbsMsgList.do?bcd=incheon&pgno={}
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
        self.channel_name = '부평구청'
        self.post_board_name = '타지역소식'