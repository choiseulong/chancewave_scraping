from celery import Celery
from celery.schedules import crontab
import importlib
import requests as req

schedule = Celery('scheduler')

# schedule.autodiscover_tasks(force=True)
# scheduler.config_from_object('./schedulerConfig')
schedule.conf.update(
    broker_url = 'amqp://username:password@localhost//',
    result_backend = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/?authSource=admin',
    timezone = 'Asia/Seoul',
    # beat_schedule = {
    #         'every-10-minute': {
    #         'task': 'scheduler.job',
    #         'schedule': crontab(minute='*/10'),
    #         'args':(1,2,3)
    #     },
    # }
)
session = req.session()
session.verify = r'./workers/dataScraper/scraperTools/FiddlerRoot.pem'
session.proxies = {
                "http": "http://127.0.0.1:8889", 
                "https":"http:127.0.0.1:8889"
            }


@schedule.task
def job(groupCode, channelCode, channelUrl, dateRange):
    scraper = importlib.import_module(f'workers.dataScraper.scraper.{groupCode}.{channelCode}').Scraper(session)
    scraper.scraping_process(channelCode, channelUrl, dateRange)
    return channelCode





