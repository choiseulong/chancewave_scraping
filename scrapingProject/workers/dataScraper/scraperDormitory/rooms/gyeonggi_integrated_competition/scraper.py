from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

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
            if self.scrapingTarget:
                self.additionalKeyValue.extend(find_request_params(self.scrapingTarget, ['Cookie'])) 
                for i in range(len(self.additionalKeyValue)):
                    del self.scrapingTarget[-(i+1)]
                self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded "))
                self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1

                #쿠키 초기화
                self.session.cookies.clear()
                self.additionalKeyValue = []
            else :
                break
    
    def post_list_scraping(self):
        super().post_list_scraping(postListParsingProcess, 'get')
    
    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess)
    





# HTTP Request
'''
    @post list 

    method : post
    url : https://www.gg.go.kr/ajax/board/getList.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    body : 
        1. bsIdx=731
        2. offset={(pageCount-1)*12}
    required data searching point :
        header_1 : fixed
        body_1 : fixed
        body_2 : pageCount
'''
'''
    @post info

    method : get
    url : https://www.gg.go.kr/bbs/boardView.do?bIdx={postSeq}&bsIdx=731&menuId=2916
    header : 
        None
    body :
        None
'''

isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl =  'https://www.gg.go.kr/bbs/boardView.do?bIdx={}&bsIdx=731&menuId=2916'
        self.channelMainUrl = 'https://www.gg.go.kr/'

    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.additionalKeyValue.append(("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"))
        self.session = set_headers(self.session, self.additionalKeyValue, isUpdate)
        self.pageCount = 0
        while True :
            self.post_list_scraping()
            if self.scrapingTarget:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else :
                break
            if self.pageCount == 1 : break
    
    def post_list_scraping(self):
        data = {
            "bsIdx" : 731,
            "offset" : (self.pageCount) * 12
        }
        super().post_list_scraping(postListParsingProcess, 'post', data)

    def target_contents_scraping(self):
        self.session = set_headers(self.session) # header 초기화
        super().target_contents_scraping(postContentParsingProcess)
