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
서울시청  
seoul_city_0  
seoul_city_1  
seoul_city_2  
(seoul_city_3 - 포스트가 각기 다른 채널로 이어져있어 추후 처리 예정)  

서울일자리포털  
job_seoul_0  
job_seoul_1    
job_seoul_2  

