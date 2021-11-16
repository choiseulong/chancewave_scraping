from workers.dataScraper.scraperDormitory.parserTools.newtools import *
from workers.scrapingScheduler.scheduler import job
import requests as req
import importlib
from configparser import ConfigParser

class ScrapingManager:
    def __init__(self):
        self.channelUrlList = []
        self.dateRange = []
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
        config.read('./workers/dataScraper/scraperTools/url.ini', encoding='utf-8')
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
        for channelCode, channelUrl in self.channelUrlList:
            groupCode = extract_groupCode(channelCode)
            # result = job.delay(groupCode, channelCode, channelUrl, self.dateRange)
            session = self.get_requests_session()
            if groupCode in ['youthcenter', 'jobaba', 'seoul_in_my_hands']:
                continue
            
            if not channelCode == 'seoul_city_0':
                continue
            
            scraperRoomPath = f'workers.dataScraper.scraperDormitory.rooms.{groupCode}.scraper'
            scraper = importlib.import_module(scraperRoomPath).Scraper(session)
            scraper.scraping_process(channelCode, channelUrl, self.dateRange)
    
    def get_date_range(self, targetDate):
        startDate = convert_datetime_string_to_isoformat_datetime(targetDate['startDate'])
        endDate = convert_datetime_string_to_isoformat_datetime(targetDate['endDate'])
        self.dateRange = [startDate, endDate]
        return self.dateRange

