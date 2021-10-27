from workers.dataScraper.parser.job_seoul import *
from workers.dataServer.mongoServer import MongoServer
from .job_seoul_0 import Scraper as job_seoul_0_Scraper
import json

class Scraper(job_seoul_0_Scraper):
    def __init__(self, session):
        super().__init__(session)
        self.contentsUrl = 'https://job.seoul.go.kr/www/custmr_cntr/ntce/WwwNotice.do?method=getWwwNews&noticeCmmnSeNo=3'