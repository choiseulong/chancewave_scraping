# CHANCEWAVE-SCRAPER

# 찬스웨이브 제공 URL 문서  
https://docs.google.com/spreadsheets/d/1cETPlC2dAQtWtms3nNYsj_MgUnK1UhopVM-DtYTvQTI/edit#gid=0  


# API 문서  
### 작성중인 문서
https://docs.google.com/spreadsheets/d/1V6YVV1Wmsp_3gtM5rJSUyqw99qMSuBOyN16DnEUOTSQ/edit?pli=1#gid=1537643233  

### 프로토타입
https://docs.google.com/spreadsheets/d/11nbCSvvK9feBZ_D-S9BXT-yNsZyT7LymKN3mFKms5aU/edit#gid=0

### 2021-12-30 제공 파일
https://docs.google.com/spreadsheets/d/16YOJfqHT-QKXYhThnxJic8iWbTYTQw1jmBhlSrsMi1Y/edit#gid=0

# Celery env  
### backend  
MONGO_URL = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/celery?authSource=admin'  

### Message Broker  
broker_url = 'pyamqp://choline:123123@localhost:8080//'  

### Run Celery
app.py 와 같은 경로에서 실행하였음 C:\workspace\scrapingProject\chancewave-scraper\scrapingProject  
celery -A workers.scraping_scheduler.scheduler worker --loglevel=info --pool=prefork --autoscale=2,8   #service
celery -A workers.scraping_scheduler.scheduler worker --loglevel=inf --pool=gevent --concurrency=12    #local dev


### Run RabbitMQ, Message Broker 
broker_url = 'pyamqp://choline:123123@localhost:8080//'  

docker run -d --name rabbitmq -p 5672:5672 -p 8080:15672 --restart=unless-stopped -e RABBITMQ_DEFAULT_USER=username -e RABBITMQ_DEFAULT_PASS=password rabbitmq:management  

## 데이터 사용시 참고사항
##### base64 기반 img 존재 - api 문서 내 표기
##### img url 요청시 Referer = {post_url}선언해야 하는 채널 
##### gimhae_0, haman_0, hygn_0
