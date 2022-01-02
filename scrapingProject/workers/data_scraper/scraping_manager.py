from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from workers.scraping_scheduler.scheduler import job
from configparser import ConfigParser
from workers.error_checker.checker import ErrorChecker
import requests as req
import importlib
from datetime import datetime, timedelta
from pytz import timezone
from glob import glob

import os

print(os.path.dirname(__file__))

SCRAPING_MANAGER_FILE_PATH = os.path.dirname(__file__)
SCRAPING_ROOMS_DIR_PATH = os.path.join(SCRAPING_MANAGER_FILE_PATH, 'scraper_dormitory', 'rooms')

URL_CONFIG_INI_PATH = os.path.join(SCRAPING_MANAGER_FILE_PATH, 'scraper_dormitory', 'scraper_tools', 'url.ini')
FIDDLER_PEM_PATH = os.path.join(SCRAPING_MANAGER_FILE_PATH, 'scraper_dormitory', 'scraper_tools', 'FiddlerRoot.pem')

# import traceback

checker = ErrorChecker()


class ScrapingManager:
    def __init__(self):
        self.channel_url_list = []
        self.date_range = []

    def get_requests_session(
            self,
            proxies={
                "http": "http://127.0.0.1:8889",
                "https": "http:127.0.0.1:8889"
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
            if 'url_' in key:
                self.channel_url_list.append((key[4:], globals()[key]))

    # def scraping_test(self, channel_code):
    #     print(channel_code)

    def scraping_worker_job_init(self):
        self.get_channel_url()

        for channel_code, channel_url in self.channel_url_list:
            group_name = extract_group_code(channel_code)
            room_name, channel_code = extract_room_name_and_channel_code(channel_code)
            tmp_room_num = channel_code.split('_')[-1]
            # job.delay(group_name, room_name, channel_code, channel_url, self.date_range)

            if channel_code != 'suncheon_0':
                continue
            print(channel_code, 'init')
            print(group_name, room_name)
            session = self.get_requests_session()

            tmp_scraper_file_name_list = get_scraper_file_list_from_group_room(group_name, room_name)

            scraper_room_address = None
            for tmp_scraper_file_name in tmp_scraper_file_name_list:

                # module 이름으로 변형 위해 python 확장자 제거
                tmp_module_nm = tmp_scraper_file_name[:tmp_scraper_file_name.rfind('.py')]
                if tmp_module_nm == f'scraper_{tmp_room_num}':
                    scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.{tmp_module_nm}'
                    break
            else:
                scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'

            scraper = importlib.import_module(scraper_room_address).Scraper(session)
            scraper.scraping_process(channel_code, channel_url, self.date_range)

    def get_date_range(self, target_date):
        start_date = convert_datetime_string_to_isoformat_datetime(target_date['start_date'])
        end_date = convert_datetime_string_to_isoformat_datetime(target_date['end_date'])
        self.date_range = [start_date, end_date]
        return self.date_range


def get_scraper_file_list_from_group_room(group_name, room_name):
    total_scraper_file_list = []
    tmp_scraper_file_path_list = glob(
        os.path.join(SCRAPING_ROOMS_DIR_PATH, group_name, room_name) + os.path.sep + 'scraper*.py')
    for tmp_scraper_file_path in tmp_scraper_file_path_list:
        tmp_file_nm = os.path.basename(tmp_scraper_file_path)
        if tmp_file_nm[-3:] != '.py':
            continue
        total_scraper_file_list.append(tmp_file_nm)

    return total_scraper_file_list


def combine_group_room_num_str(group_name, room_name, room_num):
    return group_name + '__' + room_name + '_' + room_num


def scraping_manager_runner():
    scraping_manager = ScrapingManager()
    scraping_manager.scraping_worker_job_init()


if __name__ == '__main__':
    # scraping_manager_runner()

    tmp_group_name = 'jejudo'
    tmp_room_name = 'jeju'
    tmp_room_num = '0'

    URL_CODE = combine_group_room_num_str(tmp_group_name, tmp_room_name, tmp_room_num)

    config = ConfigParser()
    config.read(URL_CONFIG_INI_PATH, encoding='utf-8')

    TARGET_URL = config['URL'][URL_CODE]

    print(config['URL'][URL_CODE])
    now = datetime.now(timezone('Asia/Seoul'))
    todayString = now.strftime('%Y-%m-%d %H:%M:%S')
    before2WeekString = (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    start_date = convert_datetime_string_to_isoformat_datetime(todayString)
    end_date = convert_datetime_string_to_isoformat_datetime(before2WeekString)

    tmp_scraper_file_name_list = get_scraper_file_list_from_group_room(group_name=tmp_group_name,
                                                                       room_name=tmp_room_name)

    scraper_room_address = None
    for tmp_scraper_file_name in tmp_scraper_file_name_list:

        # module 이름으로 변형 위해 python 확장자 제거
        tmp_module_nm = tmp_scraper_file_name[:tmp_scraper_file_name.rfind('.py')]
        if tmp_module_nm == f'scraper_{tmp_room_num}':
            print(f'{tmp_room_name} IDX {tmp_room_num}')
            scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{tmp_group_name}.{tmp_room_name}.{tmp_module_nm}'
            break
    else:
        print('NOT MATCH IDX')
        scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{tmp_group_name}.{tmp_room_name}.scraper'
    session = req.Session()
    scraper = importlib.import_module(scraper_room_address).Scraper(session)
    scraper.scraping_process(URL_CODE, TARGET_URL, [start_date, end_date])

