from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import *
from ..dataServer.mongoServer import MongoServer
import requests as req
from datetime import timedelta
import importlib
from configparser import ConfigParser

class ScrapingManager:
    def __init__(self):
        self.channelUrlList = []
        self.dataRange = []
        config = ConfigParser()
        config.read('./scraperTools/url.ini')
        for section in config.sections():
            for item in list(config[section].items()):
                key = item[0] 
                value = item[1] 
                globals()[f'{section}_{key}'] = value
    
    def get_requests_session(
            self, 
            proxies = {
                "http": "http://127.0.0.1:8889", 
                "https":"http:127.0.0.1:8889"
            }
        ):
        session = req.Session()
        session.verify = r'./workers/dataScraper/scraperTools/FiddlerRoot.pem'
        session.proxies = proxies
        return session
    
    def get_channel_url(self):
        config = ConfigParser()
        config.read('./workers/dataScraper/scraperTools/url.ini')
        for section in config.sections():
            sectionName = section.lower()
            for item in list(config[section].items()):
                key = item[0] 
                value = item[1] 
                globals()[f'{sectionName}_{key}'] = value
        for key in globals():
            if 'url_' in key :
                self.channelUrlList.append((key[4:], globals()[key]))

    def scraping_worker_job_init(self):
        self.get_channel_url()
        dataRange = self.dataRange
        for channelCode, channelUrl in self.channelUrlList[:3]:
            session = self.get_requests_session()
            scraper = importlib.import_module(f'workers.dataScraper.scraper.{channelCode}').Scraper(session)
            scraper.scraping_process(channelCode, channelUrl, dataRange)
    
    def get_date_range(self, targetDate):
        startDate = convert_datetime_string_to_actual_datetime(targetDate['startDate'])
        endDate = convert_datetime_string_to_actual_datetime(targetDate['endDate'])
        self.dataRange = [startDate, endDate]
        return self.dataRange

            