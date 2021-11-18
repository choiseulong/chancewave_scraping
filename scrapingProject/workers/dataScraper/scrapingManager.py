from workers.dataScraper.scraperDormitory.parserTools.newtools import *
from workers.scrapingScheduler.scheduler import job
from configparser import ConfigParser
from workers.errorChecker.checker import ErrorChecker
import requests as req
# import importlib
# import traceback

checker = ErrorChecker()

class ScrapingManager:
    def __init__(self):
        self.channelUrlList = []
        self.dateRange = []
    
    def get_requests_session(
            self, 
            proxies = {
                "http": "http://127.0.0.1:8889", 
                "https":"http:127.0.0.1:8889"
            }
        ):
        session = req.Session()
        # session.verify = r'./workers/dataScraper/scraperDormitory/scraperTools/FiddlerRoot.pem'
        # session.proxies = proxies
        return session

    def get_channel_url(self):
        config = ConfigParser()
        config.read('./workers/dataScraper/scraperDormitory/scraperTools/url.ini', encoding='utf-8')
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
            roomName = extract_groupCode(channelCode)
            try :
                job.delay(roomName, channelCode, channelUrl, self.dateRange)
            except Exception as e :
                print('error')
                return
                # something = checker.is_handling(traceback.format_exc(), e.__class__)
                # print(something)
            
            # if channelCode != 'youthcenter_0':
            #     continue
            
            # session = self.get_requests_session()
            # scraperRoomAddress = f'workers.dataScraper.scraperDormitory.rooms.{roomName}.scraper'
            # scraper = importlib.import_module(scraperRoomAddress).Scraper(session)
            # scraper.scraping_process(channelCode, channelUrl, self.dateRange)
    
    def get_date_range(self, targetDate):
        startDate = convert_datetime_string_to_isoformat_datetime(targetDate['startDate'])
        endDate = convert_datetime_string_to_isoformat_datetime(targetDate['endDate'])
        self.dateRange = [startDate, endDate]
        return self.dateRange

