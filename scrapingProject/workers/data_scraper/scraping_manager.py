from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from workers.scraping_scheduler.scheduler import job
from configparser import ConfigParser
from workers.error_checker.checker import ErrorChecker
import requests as req
import importlib

checker = ErrorChecker()

class ScrapingManager:
    def __init__(self):
        self.channel_url_list = []
        self.date_range = []
    
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
            section_name = section.lower()
            for item in list(config[section].items()):
                key = item[0] 
                value = item[1] 
                globals()[f'{section_name}_{key}'] = value
        for key in globals():
            if 'url_' in key :
                self.channel_url_list.append((key[4:], globals()[key]))
    
    # def scraping_test(self, channel_code):
    #     print(channel_code)

    def scraping_worker_job_init(self):
        self.get_channel_url()
        for channel_code, channel_url in self.channel_url_list:
            group_name = extract_group_code(channel_code)
            room_name, channel_code = extract_room_name_and_channel_code(channel_code)
            # job.delay(group_name, room_name, channel_code, channel_url, self.date_range)

            if channel_code != 'boseong_0':
                continue
            print(channel_code, 'init')
            print(group_name, room_name)
            session = self.get_requests_session()
            scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'
            scraper = importlib.import_module(scraper_room_address).Scraper(session)
            scraper.scraping_process(channel_code, channel_url, self.date_range)
    
    def get_date_range(self, targetDate):
        start_date = convert_datetime_string_to_isoformat_datetime(targetDate['start_date'])
        end_date = convert_datetime_string_to_isoformat_datetime(targetDate['end_date'])
        self.date_range = [start_date, end_date]
        return self.date_range


if __name__ == '__main__':
    manager = ScrapingManager()
    manager.get_channel_url()
    print(manager.channel_url_list)