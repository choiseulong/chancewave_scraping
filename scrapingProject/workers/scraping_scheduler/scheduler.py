from celery import Celery
import importlib
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util import Retry
from datetime import datetime
import traceback as tb
import logging
import json
import sys, os
from ..data_server.mongo_server import MongoServer

# python print disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
# def enablePrint():
#     sys.stdout = sys.__stdout__

# 로깅 레벨 CRITICAL로 선언 
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

#celery app
schedule = Celery('scheduler')

# celery app env
schedule.conf.update(
    broker_url = 'amqp://username:password@localhost//',
    result_backend = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/?authSource=admin',
    # broker_url = 'amqp://CHANCEWAVE:MYSTERICO@message_broker_container//',
    # result_backend = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/?authSource=admin',
    timezone = 'Asia/Seoul',
    enable_utc = False,
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
    session.headers = {
        "Connection": "keep-alive",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

# job
# 1시간 time limit 
# retry 간격 3분 디폴트
@schedule.task(time_limit=3600, retries=3)
def job(scraper_room_address, channel_code, channel_url):
    blockPrint()
    traceback = ''
    try :
        session = make_session()
        scraper = importlib.import_module(scraper_room_address).Scraper(session)
        scraper.scraping_process(channel_code, channel_url, dev=True) # 로컬 테스트 
        # scraper.scraping_process(channel_code, channel_url, dev=False)
        status = 'SUCCESS'
        traceback = None
        error_type = None
    except Exception as e:
        status = 'FAILURE'
        traceback = tb.format_exc()
        error_type = e.__class__.__name__

    return {
        'channel_code':channel_code, 
        'status':status, 
        'date_done':datetime.now().isoformat(), 
        'traceback':traceback,
        'error_type' : error_type
    }
