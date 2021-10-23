# chancewave-scraper
#### 원본 url 문서
https://docs.google.com/spreadsheets/d/1HsEMGsDaFKClZJ4_oiR9DgcKSzp-gx8Jypyw2rBWRSs/edit#gid=1281475338

#### 새로운 채널 추가하기 
###### 10/23, 18:20
method : post
url : http://localhost:8000/add-new-target-channel
body : 
{
    "channelName" : "서울시청",
    "channelUrl" : [
        "https://www.seoul.go.kr/realmnews/in/list.do", 
        "https://www.seoul.go.kr/thismteventfstvl/list.do", 
        "https://www.seoul.go.kr/eventreqst/list.do", 
        "http://rss.seoul.go.kr/app/rss/board/list/0/0"
    ]
}
채널 url 코드 생성 후 반영

![newchannelinit](https://user-images.githubusercontent.com/48904372/138550628-7f5b0e4d-70ce-4ce6-8811-362033f7b402.png)

