# chancewave-scraper
#### 원본 url 문서
https://docs.google.com/spreadsheets/d/1HsEMGsDaFKClZJ4_oiR9DgcKSzp-gx8Jypyw2rBWRSs/edit#gid=1281475338


#### api 문서
https://www.notion.so/mysterico/API-ef38832851e94bf781edddde026ea0ea


##### body 를 비워두고 요청할 시 요청 날짜부터 7일 이전까지를 타겟 범위로 정함
##### startDate 는 endDate 보다 상대적으로 최근 날짜입니다.
url : scraping-start-with-date  
method : post  
body : {  
    #optional  (상대적 최근 날짜)이날부터
    "startDate" : "2021-10-26",  --> "%Y-%m-%d"  
    #optional  (상대적 과거 날짜)이날까지
    "endDate" : "2021-10-01",  --> "%Y-%m-%d"  
}  

##### base64 img read using python
import base64  

with open("yourfile.ext", "rb") as image_file:  
      encoded_string = base64.b64encode(image_file.read())  

# 처리된 ChannleCode 표기
<!-- 서울시청  
서울일자리포털  
서울우먼업  
서울부동산정보광장  
서울특별시평생학습포털  
서울복지포털   -->

서울우먼업  
온라인청년센터  
경기도 자바바  
 
## fixed
postUrl 특정이 불가할 시 해당 채널은 모든 데이터를 재수집 하는 방향으로 설정함.

#### backend  
MONGO_URL = 'mongodb://admin:mysterico@k8s.mysterico.com:31489/celery?authSource=admin'  

#### message broker  
broker_url = 'pyamqp://choline:123123@localhost:8080//'  

#### run celery
celery -A tasks worker --loglevel=info --pool=solo --concurrency=24  

#### run rabbitmq
docker run -d --name rabbitmq -p 5672:5672 -p 8080:15672 --restart=unless-stopped -e RABBITMQ_DEFAULT_USER=username -e RABBITMQ_DEFAULT_PASS=password rabbitmq:management  

task1 = taskFun.delay(인자)  
task2 = taskFun.apply_async(args=[인자], kwargs={인자})  

task1 = taskFun.s(인자) 혹은  taskFun.s()  
task1 = taskFun.subtask(인자) 혹은  taskFun.subtask()  

이후  

delay 혹은 apply_async로 실행함  
subtask에서 Arguments를 이미 정의했다면했기  

delay 및 apply_async로 추가 전달할 경우 Append됨.  

subtask를 처리할 때 **chain**을 사용하여 연속된 Task를 처리하고,  

**chord**를 사용하여 일괄처리 할 수 있다.  

task1.ready() → true : 완료, false : 진행중  

참고 : https://heodolf.tistory.com/66?category=897877  
스케쥴 예약 참고 : https://wangin9.tistory.com/entry/django-celery  


## 추후처리
celery -A scheduler beat  
celery -A workers.scrapingScheduler.scheduler worker --loglevel=info -P gevent -c 24  
app실행시 같이 시작되게끔  