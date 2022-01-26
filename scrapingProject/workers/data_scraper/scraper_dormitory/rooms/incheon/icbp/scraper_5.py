from .scraper import Scraper as default_scraper

# 채널 이름 : 부평구청평생학습관

#HTTP Request
'''
    @post list
    method : GET
    url = https://www.icbp.go.kr/welfare/bbs/bbsMsgList.do?bcd=welfare_news&pgno={}
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
        self.channel_name = '부평구청평생학습관'
        self.post_board_name = '공지사항'