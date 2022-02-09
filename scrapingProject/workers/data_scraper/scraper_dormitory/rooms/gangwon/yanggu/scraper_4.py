from .scraper_3 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 =  https://www.yanggu.go.kr/user_sub.php?gid=health&bcd=news&mu_idx=70&pg={}
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
        self.channel_name = '양구군보건소'
        self.post_board_name = '새소식/공지사항'
        self.post_url = 'https://www.yanggu.go.kr/'