from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 원자력안전위원회

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url = https://www.nssc.go.kr/ajaxf/FR_BBS_SVC/BBSViewList.do
    header :
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. pageNo = {pageCount}
        2. pagePerCnt = 15
        3. MENU_ID = 180
        4. SITE_NO = 2
        5. BOARD_SEQ = 4

    required data searching point :
        header_1 : fixed
        body_1 : {pageCount}
        body_other : fixed

'''
'''
    @post info
    method : POST
    url : https://www.nssc.go.kr/ajaxf/FR_BBS_SVC/BoardViewData.do
    header :
        None
    body : 
        data = {
            "MENU_ID" : 180,
            "SITE_NO" : 2,
            "BOARD_SEQ" : 4, 
            "BBS_SEQ" : {postId}
        }
    required data searching point :
        header_1 : fixed
        body_1 = {nttId}
'''

sleepSec = 3
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '원자력안전위원회'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'https://www.nssc.go.kr'
        self.postUrl = 'https://www.nssc.go.kr/ajaxf/FR_BBS_SVC/BoardViewData.do'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.postUrlFrame = 'https://www.nssc.go.kr/ko/cms/FR_BBS_CON/BoardView.do?MENU_ID=180&CONTENTS_NO=&SITE_NO=2&BOARD_SEQ=4&BBS_SEQ={}'
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            self.post_list_scraping()
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else :
                break
            
    def post_list_scraping(self):
        data = {
            "pageNo" : self.pageCount,
            "pagePerCnt" : 15 ,
            "MENU_ID" : 180,
            "SITE_NO" : 2,
            "BOARD_SEQ" :4
        }
        super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)


            

 



