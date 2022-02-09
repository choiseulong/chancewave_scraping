from .scraper import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.samcheok.go.kr/specialty/00466/01314.web?gcode=1002&cpage={}
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
'''
    이미지 요청시 Referer 로 post_url 전송 필요
    sleep_sec을 늘려야함
'''

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '삼척시청'
        self.post_board_name = '건강/보건/새소식'
        self.post_url = 'https://www.samcheok.go.kr/specialty/00466/01314.web'