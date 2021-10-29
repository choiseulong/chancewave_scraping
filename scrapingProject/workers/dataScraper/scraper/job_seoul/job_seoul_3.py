from workers.dataScraper.parser.job_seoul import *
from workers.dataServer.mongoServer import MongoServer
from .job_seoul_2 import Scraper as job_seoul_3_Scraper
import json

class Scraper(job_seoul_3_Scraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://job.seoul.go.kr/www/training/elder_training'
        self.additinalHeaderElement = []
        self.extract_post_list_from_response_text = other_extract_post_list_from_response_text
        self.extract_post_contents_from_response_text = other_extract_post_contents_from_response_text