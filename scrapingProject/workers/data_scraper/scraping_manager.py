from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from workers.scraping_scheduler.scheduler import job
from configparser import ConfigParser
from workers.error_checker.checker import error_checker
import requests as req
import importlib
# import traceback

checker = error_checker()

class scraping_manager:
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
        session.verify = r'./workers/data_scraper/scraper_dormitory/scraper_tools/FiddlerRoot.pem'
        session.proxies = proxies
        return session

    def get_channel_url(self):
        config = ConfigParser()
        config.read('./workers/data_scraper/scraper_dormitory/scraper_tools/url.ini', encoding='utf-8')
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
            # channelCode = main_site__youthcenter_0
            # groupName = main_site
            # roomName = youthcenter
            # channelCode = youthcenter_0
            groupName = extract_groupCode(channelCode)
            roomName, channelCode = extract_roomName_and_channelCode(channelCode)
            # job.delay(roomName, channelCode, channelUrl, self.dateRange)
            # try :
            #     job.delay(roomName, channelCode, channelUrl, self.dateRange)
            # except Exception as e :
            #     print('error')
            #     return
                # something = checker.is_handling(traceback.format_exc(), e.__class__)
                # print(something)
            
            if channelCode != 'gumi_0':
                continue
            print(channelCode, 'init')
            print(groupName, roomName)
            session = self.get_requests_session()
            scraperRoomAddress = f'workers.data_scraper.scraper_dormitory.rooms.{groupName}.{roomName}.scraper'
            scraper = importlib.import_module(scraperRoomAddress).Scraper(session)
            scraper.scraping_process(channelCode, channelUrl, self.dateRange)
    
    def get_date_range(self, targetDate):
        startDate = convert_datetime_string_to_isoformat_datetime(targetDate['startDate'])
        endDate = convert_datetime_string_to_isoformat_datetime(targetDate['endDate'])
        self.dateRange = [startDate, endDate]
        return self.dateRange

