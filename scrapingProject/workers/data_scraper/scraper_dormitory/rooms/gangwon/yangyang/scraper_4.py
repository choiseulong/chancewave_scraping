from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.yangyang.go.kr/gw/portal/yyc_partinfo_edu_female_infoedu?mode=listForm&boardCode=BDAABB33&curPage={}
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
        self.channel_name = '양양여성회관'
        self.post_board_name = '교육안내'
        self.post_url = 'https://www.yangyang.go.kr/gw/portal/yyc_partinfo_edu_female_infoedu?mode=readForm&boardCode=BDAABB33&articleSeq={}'