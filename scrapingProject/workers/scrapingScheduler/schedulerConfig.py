from celery.schedules import crontab

broker_url = 'amqp://username:password@localhost//'
result_backend = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/?authSource=admin'
TIME_ZONE = 'Asia/Seoul'

beat_schedule = {
    'every-10-minute': {
        'task': 'scheduler.scraping',
        'schedule': crontab(minute='*/10'),
    },
}