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
    #optional  (상대적 최근 날짜)이날부터
    "startDate" : "2021-10-26",  --> "%Y-%m-%d"  
    #optional  (상대적 과거 날짜)이날까지
    "endDate" : "2021-10-01",  --> "%Y-%m-%d"  
}  

# 처리된 ChannleCode : Url
seoul_city_0 = https://www.seoul.go.kr/realmnews/in/list.do  
seoul_city_1 = https://www.seoul.go.kr/thismteventfstvl/list.do  
seoul_city_2 = https://www.seoul.go.kr/eventreqst/list.do  
seoul_city_3 # 포스트가 각기 다른 채널로 이어져있어 추후 처리 예정 #

job_seoul_0 : https://job.seoul.go.kr/www/custmr_cntr/ntce/WwwNotice.do?method=selectWwwNoticeList&pageIndex={}  
job_seoul_1 : https://job.seoul.go.kr/www/custmr_cntr/ntce/WwwNotice.do?method=selectNewsList&noticeCmmnSeNo=3&pageIndex={}


