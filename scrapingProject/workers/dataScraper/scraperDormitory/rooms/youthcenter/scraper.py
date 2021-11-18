from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# SCRAPER
# youthcenter_0 : 청년정책 통합검색
# 타겟 : 모든 포스트
# 중단 시점 : 유효 포스트가 0개인 경우가 5번 연속 나올 경우

# HTTP Request
'''
    @post list 

    method : get
    url : https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1
    header : none
'''
'''
    @post info

    method : post
    url : https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded 
        2. Cookie: YOUTHCENTERSESSIONID=CjoODAtum_PuuKthsJaMypZLqg4b5HlmNsEt8eKzphA686yPkRR_!1041055556!1126342983;
    body :
        _csrf=072abdbd-ecab-4fcb-bb99-5acec3572242&bizId=R2021021800010
        1. _csrf=04baa83b-492c-415c-9820-94ab677331a9
        2. bizId=R2021021800010
    required data searching point :
        header_1 : fixed
        header_2 : dynamic 
            get <@post list> header Cookie and parsing
        body_1 : dynamic 
            find <@post list> html tag attrs['content']
                <meta name="_csrf" content="04baa83b-492c-415c-9820-94ab677331a9" />
        body_2 : dynamic 
            find <@post list> html tag attrs['value'] and parsing
                <span class="checkbox">
						<input type="checkbox" class="checkbox" id="cmprCheckboxR2021021800010" name="cmprCheckbox" value="R2021021800010">
						<label for="cmprCheckboxR2021021800010"><span class="blind"><em>국민취업지원제도</em>선택</span></label>
                </span>	
'''
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do'

    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.mongo.remove_channel_data(channelCode)
        self.pageCount = 1
        while True :
            self.session = set_headers(self.session)
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            self.post_list_scraping()
            if isinstance(self.scrapingTarget, list):
                self.additionalKeyValue.extend(find_request_params(self.scrapingTarget, ['Cookie'])) 
                for i in range(len(self.additionalKeyValue)):
                    del self.scrapingTarget[-(i+1)]
                self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded "))
                self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
                self.emptyPageCount = 0

                #쿠키 초기화
                self.session.cookies.clear()
                self.additionalKeyValue = []
            elif self.scrapingTarget == 'endpoint' : break
                
    
    def post_list_scraping(self):
        super().post_list_scraping(postListParsingProcess, 'get')
    
    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess)
    



