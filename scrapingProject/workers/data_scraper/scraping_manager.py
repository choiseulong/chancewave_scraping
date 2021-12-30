from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from workers.scraping_scheduler.scheduler import job
from configparser import ConfigParser
from workers.error_checker.checker import ErrorChecker
import requests as req
import importlib
from datetime import datetime, timedelta
from pytz import timezone

import os
print(os.path.dirname(__file__))

URL_CONFIG_INI_PATH = os.path.join(os.path.dirname(__file__), 'scraper_dormitory', 'scraper_tools', 'url.ini')
FIDDLER_PEM_PATH = os.path.join(os.path.dirname(__file__), 'scraper_dormitory', 'scraper_tools', 'FiddlerRoot.pem')

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
        session.verify = FIDDLER_PEM_PATH
        session.proxies = proxies
        return session

    def get_channel_url(self):
        config = ConfigParser()
        config.read(URL_CONFIG_INI_PATH, encoding='utf-8')
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

            if channel_code != 'jangheung_0':
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


def combine_group_room_num_str(group_name, room_name, room_num):
    return group_name + '__' + room_name + '_' + room_num


if __name__ == '__main__':

    tmp_group_name = 'gyeonggi'
    tmp_room_name = 'gyeonggido'
    tmp_room_num = '0'

    URL_CODE = combine_group_room_num_str(tmp_group_name, tmp_room_name, tmp_room_num)

    config = ConfigParser()
    config.read(URL_CONFIG_INI_PATH, encoding='utf-8')

    TARGET_URL = config['URL'][URL_CODE]

    print(config['URL'][URL_CODE])
    now = datetime.now(timezone('Asia/Seoul'))
    todayString = now.strftime('%Y-%m-%d %H:%M:%S')
    before2WeekString = (now-timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    start_date = convert_datetime_string_to_isoformat_datetime(todayString)
    end_date = convert_datetime_string_to_isoformat_datetime(before2WeekString)

    scraperRoomAddress = f'workers.data_scraper.scraper_dormitory.rooms.{tmp_group_name}.{tmp_room_name}.scraper'
    proxies = {
        "http": "http://127.0.0.1:8889",
        "https": "http:127.0.0.1:8889"
    }

    session = req.Session()
    # session.verify = FIDDLER_PEM_PATH
    # session.proxies = proxies

    scraper = importlib.import_module(scraperRoomAddress).Scraper(session)
    scraper.scraping_process(URL_CODE, TARGET_URL, [start_date, end_date])

