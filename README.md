# chancewave-scraper
#### 원본 url 문서
https://docs.google.com/spreadsheets/d/1HsEMGsDaFKClZJ4_oiR9DgcKSzp-gx8Jypyw2rBWRSs/edit#gid=1281475338


#### api 문서
https://www.notion.so/mysterico/API-ef38832851e94bf781edddde026ea0ea


#### 수집 포스트 업로드 시각 유효성 체크

##### body 를 비워두고 요청할 시 요청 날짜부터 14일 이전까지를 타겟 범위로 정함

url : scraping-start-with-date  
method : post  
body : {  
    #optional  
    "startDate" : "2021-10-26",  --> "%Y-%m-%d"  
    #optional  
    "endDate" : "2021-10-01",  --> "%Y-%m-%d"  
}  