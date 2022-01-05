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
        self.channel_url_info_dict = {}
        self.date_range = []
    
    def get_requests_session(
            self, 
            proxies = {
                "http": "http://127.0.0.1:8889", 
                "https":"http:127.0.0.1:8889"
            }
        ):
        #test 시에 사용되는 session을 만든다.
        session = req.Session()
        session.verify = FIDDLER_PEM_PATH
        session.proxies = proxies
        return session

    def get_channel_url(self):
        # url.ini에 작성된 채널 URL정보를 가져와 변수에 담는다
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
                self.channel_url_info_dict.update({key[4:] : globals()[key]})

    def scraping_dev_test(self, channel_code):
        # ulsansi_0 등의 채널코드를 받아 테스트 스크래핑을 시작한다

        if not self.channel_url_info_dict :
            self.get_channel_url()
        channel_code_with_location = self.find_channel_code_with_location(channel_code)
        group_name, room_name, channel_code, channel_url = self.parse_scraping_parameters(channel_code_with_location)
        print(channel_code, 'init')
        print(group_name, room_name)
        session = self.get_requests_session()
        scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'
        scraper = importlib.import_module(scraper_room_address).Scraper(session)
        scraper.scraping_process(channel_code, channel_url)
    
    def scraping_init_with_celery(self):
        # celery 에게 스크래핑 진행을 위임한다
        for channel_code_with_location in self.channel_url_info_dict:
            group_name, room_name, channel_code, channel_url = self.parse_scraping_parameters(channel_code_with_location)
            job.delay(group_name, room_name, channel_code, channel_url)

    def parse_scraping_parameters(self, channel_code_with_location):
        # 지역정보가 함께 담긴 채널 코드를 가져와서 파싱하고 return 한다
        # channel_code_with_location = ulsan__ulsansi_0의 경우
        # group_name = ulsan, room_name = ulsansi, channel_code = ulsansi_0, 
        # channel_url = channel_url_info_dict[channel_code_with_location]
        group_name = extract_group_code(channel_code_with_location)
        room_name, channel_code = extract_room_name_and_channel_code(channel_code_with_location)
        channel_url = self.channel_url_info_dict[channel_code_with_location]
        return group_name, room_name, channel_code, channel_url

    def find_channel_code_with_location(self, channel_code):
        # 개별 채널 스크래퍼 테스트시 사용한다
        # channel_code = ulsansi_0 로 받은 경우
        # 반환값은 channel_code_with_location = ulsan__ulsansi_0 이다
        for channel_code_with_location in self.channel_url_info_dict.keys():
            if channel_code in channel_code_with_location :
                return channel_code_with_location

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
    # now = datetime.now(timezone('Asia/Seoul'))
    # todayString = now.strftime('%Y-%m-%d %H:%M:%S')
    # before2WeekString = (now-timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    # start_date = convert_datetime_string_to_isoformat_datetime(todayString)
    # end_date = convert_datetime_string_to_isoformat_datetime(before2WeekString)

    scraperRoomAddress = f'workers.data_scraper.scraper_dormitory.rooms.{tmp_group_name}.{tmp_room_name}.scraper'
    proxies = {
        "http": "http://127.0.0.1:8889",
        "https": "http:127.0.0.1:8889"
    }

    session = req.Session()
    # session.verify = FIDDLER_PEM_PATH
    # session.proxies = proxies

    scraper = importlib.import_module(scraperRoomAddress).Scraper(session)
    # scraper.scraping_process(URL_CODE, TARGET_URL, [start_date, end_date])
    scraper.scraping_process(URL_CODE, TARGET_URL)


