from celery import Celery
import importlib
from requests import Session
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util import Retry
from datetime import datetime
from pytz import timezone
import logging

# 로깅 레벨 CRITICAL로 선언 
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

#celery app
schedule = Celery('scheduler')

# celery app env
schedule.conf.update(
    # broker_url = 'amqp://username:password@localhost//',
    # result_backend = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/?authSource=admin',
    broker_url = 'amqp://CHANCEWAVE:MYSTERICO@message_broker_container//',
    result_backend = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/?authSource=admin',
    timezone = 'Asia/Seoul',

    # 2021-12-31 추가
    broker_heartbeat=None
)

# session
def make_session():
    retries_num = 3 
    backoff_factor = 1.5
    status_forcelist = (500, 400)

    retry = Retry(
        total = retries_num,
        read = retries_num,
        connect = retries_num,
        backoff_factor = backoff_factor,
        status_forcelist = status_forcelist
    )

    session = Session()
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

# job
# 10시간 time limit 
# retry 간격 3분 디폴트
@schedule.task(time_limit=36000, retries=3)
def job(group_name, room_name, channel_code, channel_url):
    startTime = datetime.now(timezone('Asia/Seoul')).isoformat()
    session = make_session()
    scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'
    scraper = importlib.import_module(scraper_room_address).Scraper(session)
    scraper.scraping_process(channel_code, channel_url)
    endTime = datetime.now(timezone('Asia/Seoul')).isoformat()
    return {
        "channel_code" : channel_code,
        "startTime" : startTime,
        "endTime" : endTime
    }





