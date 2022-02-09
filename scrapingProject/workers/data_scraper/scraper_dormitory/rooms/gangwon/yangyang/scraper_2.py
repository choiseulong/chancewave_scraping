from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.yangyang.go.kr/gw/portal/yyc_news_othernews?mode=listForm&boardCode=BDAABB05&curPage={}
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
        self.channel_name = '양양군청'
        self.post_board_name = '타기관공고/고시'
        self.post_url = 'https://www.yangyang.go.kr/gw/portal/yyc_news_othernotifi?mode=readForm&boardCode=BDAABB16&articleSeq={}'