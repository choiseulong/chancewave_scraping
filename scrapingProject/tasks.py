from celery import Celery
import time

import celery

BROKER_URL = "mongodb://admin:mysterico@k8s.mysterico.com:31489"

celery = Celery('EOD_TASKS', broker=BROKER_URL)

celery.config_from_object('celeryconfig')

@celery.task
def add(x,y):
    time.sleep(5)
    return x+y

