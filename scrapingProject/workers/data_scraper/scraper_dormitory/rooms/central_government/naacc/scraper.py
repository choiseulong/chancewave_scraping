from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 행정중심복합도시건설청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.naacc.go.kr/csi_board/csi_boardList.do?menu_id=notice&currentPage={}
    header :
        Cookie : JSESSIONID=CzmAdk8thWocQB7+1BnaZayp.node10
    required data searching point :
        header_1 : 메인페이지에서 쿠키 받아옴
'''
'''
    @post info
    method : GET
    url : https://www.naacc.go.kr/csi_board/csi_boardView.do?menu_id=notice&num={postId}
    header :
        Cookie : JSESSIONID=CzmAdk8thWocQB7+1BnaZayp.node10
    required data searching point :
        header_1 : 메인페이지에서 쿠키 받아옴
'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '행정중심복합도시건설청'
        self.postBoardName = '알립니다'
        self.channelMainUrl = 'https://www.naacc.go.kr'
        self.postUrl = 'https://www.naacc.go.kr/csi_board/csi_boardView.do?menu_id=notice&num={}'
        
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
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
        if self.pageCount == 1 :
            status, response = get_method_response(self.session, self.channelMainUrl)
            if status == 'ok' :
                JSESSIONID = response.cookies.get_dict()['JSESSIONID']
                self.additionalKeyValue.append(("Cookie", f"JSESSIONID={JSESSIONID}"))
                self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)