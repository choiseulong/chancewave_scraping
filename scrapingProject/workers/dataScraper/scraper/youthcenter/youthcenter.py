from workers.dataScraper.scraper.topLevelScrper import Scraper as ABCScraper
from workers.dataScraper.parser.youthcenter import *

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
            find <@post list> html tag attrs['onclick'] and parsing
                <a href="#" id="dtlLink_R2021021800010" onclick="f_Detail('R2021021800010');">	
'''

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do'

    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)

        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            self.post_list_scraping()


