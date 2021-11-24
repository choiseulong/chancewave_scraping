# CHANCEWAVE-SCRAPER

# 찬스웨이브 API 문서  
https://docs.google.com/spreadsheets/d/1cETPlC2dAQtWtms3nNYsj_MgUnK1UhopVM-DtYTvQTI/edit#gid=0


# 미스테리코 작성중 API 문서  
https://docs.google.com/spreadsheets/d/1V6YVV1Wmsp_3gtM5rJSUyqw99qMSuBOyN16DnEUOTSQ/edit#gid=1537643233


# HTTP Requests

url : scraping-start-with-date  
method : post  
body : {  
    #optional  (상대적 최근 날짜)이날부터
    "startDate" : "2021-10-26",  --> "%Y-%m-%d"  
    #optional  (상대적 과거 날짜)이날까지
    "endDate" : "2021-10-01",  --> "%Y-%m-%d"  
}

#  

# Celery env
#### backend  
MONGO_URL = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/celery?authSource=admin'  

#### Message Broker  
broker_url = 'pyamqp://choline:123123@localhost:8080//'  

#### Run Celery
celery -A tasks worker --loglevel=info --pool=solo --concurrency=24  

#### Run RabbitMQ
docker run -d --name rabbitmq -p 5672:5672 -p 8080:15672 --restart=unless-stopped -e RABBITMQ_DEFAULT_USER=username -e RABBITMQ_DEFAULT_PASS=password rabbitmq:management  

#

# 데이터 사용시 참고사항

##### base64 기반 img 존재
 