from .scraper_6 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.gwgs.go.kr/prog/bbsArticle/BBSMSTR_000000000408/list.do?pageIndex={}
    header :
        None
'''
'''
    @post info
    method : GET
    url : 
        self.post_url.format(post_id)
    header :
        None
'''
class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '고성군보건소'
        self.post_board_name = '새소식'
        self.post_url = 'https://www.gwgs.go.kr/prog/bbsArticle/BBSMSTR_000000000408/view.do?nttId={}'