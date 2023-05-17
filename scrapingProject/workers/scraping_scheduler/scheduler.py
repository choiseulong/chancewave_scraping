from celery import Celery
import importlib
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util import Retry
from datetime import datetime
from pytz import timezone
import traceback as tb
import logging
import json
from ..data_server.mongo_server import MongoServer

# 로깅 레벨 CRITICAL로 선언 
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

#celery app
schedule = Celery('scheduler')

# celery app env
schedule.conf.update(
    # broker_url = 'amqp://CHANCEWAVE:MYSTERICO@message_broker_container//',
    # result_backend = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/?authSource=admin',
    broker_url = 'amqp://CHANCEWAVE:MYSTERICO@211.42.153.221:5672//', # network 모드 변경에 따른 ip 변경 대응
    result_backend = 'mongodb://CHANCEWAVE:MYSTERICO@211.42.153.221:9202/?authSource=admin', # network 모드 변경에 따른 ip 변경 대응

    timezone = 'Asia/Seoul',
    enable_utc = False,
    # 2021-12-31 추가
    broker_heartbeat=None,
    task_acks_late = True, # add CELERY_ACKS_LATE-> rename newly
    # worker_prefetch_multiplier = 1
    broker_connection_retry = True,
    # broker_connection_max_retries = 0
    broker_transport_options = {"visibility_timeout" : 7200}
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
    session.headers = {
        "Connection": "keep-alive",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        # "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    }   
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

# job
# 3시간 time limit 
# retry 간격 3분 디폴트
@schedule.task(time_limit=10800, retries=3)
def job(scraper_room_address, channel_code, channel_url, full_channel_code):
    print(full_channel_code)
    dev = False
    mongo = MongoServer(dev=dev)
    traceback = ''
    try :
        session = make_session()
        scraper = importlib.import_module(scraper_room_address).Scraper(session)
        # scraper.scraping_process(channel_code, channel_url, dev=dev, full_channel_code=full_channel_code) # 로컬 테스트 
        scraper.scraping_process(channel_code, channel_url, dev=dev, full_channel_code=full_channel_code)
        status = 'SUCCESS'
        traceback = None
        error_type = None
    except Exception as e:
        status = 'FAILURE'
        traceback = tb.format_exc()
        error_type = e.__class__.__name__

    history = {
        'channel_code':channel_code, 
        'status':status, 
        'date_done':datetime.now(timezone('Asia/Seoul')).isoformat(), 
        'traceback':traceback,
        'error_type' : error_type
    }
    mongo.write_scraping_history(history)
    return full_channel_code