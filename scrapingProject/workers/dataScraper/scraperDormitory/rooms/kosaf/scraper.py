from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 드림스폰

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시


#HTTP Request
'''
    @post list

    method : GET
    url = https://www.dreamspon.com/scholarship/list.html?page={pageCount}
    header :
        None
'''
'''
    @post info
    method : GET
    url : https://www.gcon.or.kr/busiNotice/view?pageNum=1&rowCnt=10&linkId={linkId}&menuId=MENU02369
    header :
        User-Agent
    required data searching point :
        header_1 : fixed
'''

sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'https://www.dreamspon.com'
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.pageCount = 4
        status = self.login_process()
        if status :
            while True :
                self.session = set_headers(self.session)
                self.channelUrl = self.channelUrlFrame.format(self.pageCount)
                self.post_list_scraping()
                if self.scrapingTarget :
                    self.target_contents_scraping()
                    self.collect_data()
                    self.mongo.reflect_scraped_data(self.collectedDataList)
                    self.pageCount += 1
                else :
                    break
                if self.pageCount == 5:
                    break
 
    def post_list_scraping(self):
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)
    
    def login_process(self):
        url = 'https://www.dreamspon.com/process/checkuser.html'
        data = {
            "mode" : "login",
            "userid" : "chancewave@mysterico.com",
            "pageReferer" : 'https://www.dreamspon.com/',
            "userpw" : "mysterico"
        }
        self.session = set_headers(self.session, ['Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'], isUpdate)
        _, response = post_method_response(self.session, url, data)
        if response.json()['checkyn'] == 'Y' :
            return True
        else :
            return False
       



            

 



