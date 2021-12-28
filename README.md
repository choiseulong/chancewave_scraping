# CHANCEWAVE-SCRAPER

# 찬스웨이브 API 문서  
https://docs.google.com/spreadsheets/d/1cETPlC2dAQtWtms3nNYsj_MgUnK1UhopVM-DtYTvQTI/edit#gid=0


# 미스테리코 작성중 API 문서  
https://docs.google.com/spreadsheets/d/1V6YVV1Wmsp_3gtM5rJSUyqw99qMSuBOyN16DnEUOTSQ/edit#gid=1537643233

https://docs.google.com/spreadsheets/d/11nbCSvvK9feBZ_D-S9BXT-yNsZyT7LymKN3mFKms5aU/edit#gid=0


# HTTP Requests

url : scraping-start-with-date  
method : post  
body : {  
    #optional  (상대적 최근 날짜)이날부터
    "start_date" : "2021-10-26",  --> "%Y-%m-%d"  
    #optional  (상대적 과거 날짜)이날까지
    "end_date" : "2021-10-01",  --> "%Y-%m-%d"  
}

#  

# Celery env
#### backend  
MONGO_URL = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/celery?authSource=admin'  

#### Message Broker  
broker_url = 'pyamqp://choline:123123@localhost:8080//'  

#### Run Celery
(venv) PS C:\workspace\scrapingProject\chancewave-scraper\scrapingProject> celery -A workers.scraping_scheduler.scheduler worker --loglevel=info --pool=solo --concurrency=24

 -------------- celery@DESKTOP-0QP09FD v5.2.0 (dawn-chorus)
--- ***** -----
-- ******* ---- Windows-10-10.0.19041-SP0 2021-12-27 11:51:57
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         scheduler:0x125ff2f83c8
- ** ---------- .> transport:   amqp://username:**@localhost:5672//
- ** ---------- .> results:     mongodb://admin:**@k8s.mysterico.com:31489/
- *** --- * --- .> concurrency: 24 (solo)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . workers.scraping_scheduler.scheduler.job

[2021-12-27 11:51:57,723: INFO/MainProcess] Connected to amqp://username:**@127.0.0.1:5672//
[2021-12-27 11:51:57,748: INFO/MainProcess] mingle: searching for neighbors
[2021-12-27 11:51:58,801: INFO/MainProcess] mingle: all alone
[2021-12-27 11:51:58,817: INFO/MainProcess] celery@DESKTOP-0QP09FD ready.


#### Run RabbitMQ
docker run -d --name rabbitmq -p 5672:5672 -p 8080:15672 --restart=unless-stopped -e RABBITMQ_DEFAULT_USER=username -e RABBITMQ_DEFAULT_PASS=password rabbitmq:management  

## 데이터 사용시 참고사항

##### base64 기반 img 존재 - api 문서 내 표기
##### img url 요청시 Referer = {post_url}선언해야 하는 채널이 존재 
##### gimhae_0, haman_0, hygn_0
