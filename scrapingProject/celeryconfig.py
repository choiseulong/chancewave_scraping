from celery.schedules import crontab

result_backend = "mongodb://admin:mysterico@k8s.mysterico.com:31489"
mongodb_backend_settings = {
    "database": "chancewave_scraper", 
    "taskmeta_collection": "backend",
}

beat_schedule = {
        'every-minute': {
        'task': 'tasks.add',
        'schedule': crontab(minute='*/1'),
        'args': (1,2),
    },
}