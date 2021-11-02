from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parser.seoul_woman_up import *
from workers.dataServer.mongoServer import MongoServer
from .seoul_woman_up_0 import Scraper as default_scraper

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://www.seoulwomanup.or.kr/womanup/common/bbs/selectBBS.do?bbs_seq={}&bbs_code=centerall'
