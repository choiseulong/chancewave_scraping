from .scraper_1 import Scraper as default_scraper
'''
    @post list
    method : GET
    url_0 = https://www.gwgs.go.kr/prog/lecCourse/EMD/sub06_090601/list.do?pageIndex={}
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
        self.channel_name = '고성군청'
        self.post_board_name = '읍면주민자치프로그램'
        