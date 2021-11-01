from celery import Celery
import redis

rd = redis.StrictRedis(host = 'localhost', port=6379, db=0)
rd.set("test", "hello")

# app = Celery('task', broker='redis://localhost:6379//')