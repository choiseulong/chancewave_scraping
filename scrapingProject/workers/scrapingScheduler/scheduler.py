from celery import Celery
import importlib
import requests as req

schedule = Celery('scheduler')

# schedule.autodiscover_tasks(force=True)
# scheduler.config_from_object('./schedulerConfig')
schedule.conf.update(
    # broker_url = 'amqp://username:password@localhost//',
    # result_backend = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/?authSource=admin',
    broker_url = 'amqp://CHANCEWAVE:MYSTERICO@message_broker_container//',
    result_backend = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/?authSource=admin',
    timezone = 'Asia/Seoul',
)

@schedule.task
def job(roomName, channelCode, channelUrl, dateRange):
    session = req.session()
    scraperRoomAddress = f'workers.dataScraper.scraperDormitory.rooms.{roomName}.scraper'
    scraper = importlib.import_module(scraperRoomAddress).Scraper(session)
    scraper.scraping_process(channelCode, channelUrl, dateRange)
    return channelCode





