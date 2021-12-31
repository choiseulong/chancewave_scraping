from celery import Celery
import importlib
import requests as req
from datetime import datetime
from pytz import timezone

schedule = Celery('scheduler')

schedule.conf.update(
    broker_url = 'amqp://username:password@localhost//',
    # result_backend = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/?authSource=admin',
    broker_url = 'amqp://CHANCEWAVE:MYSTERICO@message_broker_container//',
    result_backend = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/?authSource=admin',
    timezone = 'Asia/Seoul',
)

@schedule.task
def job(group_name, room_name, channel_code, channel_url, date_range):
    startTime = datetime.now(timezone('Asia/Seoul')).isoformat()
    session = req.session()
    scraper_room_address = f'workers.data_scraper.scraper_dormitory.rooms.{group_name}.{room_name}.scraper'
    scraper = importlib.import_module(scraper_room_address).Scraper(session)
    scraper.scraping_process(channel_code, channel_url, date_range)
    endTime = datetime.now(timezone('Asia/Seoul')).isoformat()
    return {
        "channel_code" : channel_code,
        "startTime" : startTime,
        "endTime" : endTime
    }





