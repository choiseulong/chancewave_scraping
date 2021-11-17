from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *


# SCRAPER
# seoul_city_0
# seoul_city_1
# seoul_city_2

#HTTP Request

'''
    @post list

    method : post
    url = https://www.seoul.go.kr/realmnews/in/list.do
    header :
        1. User-Agent
    body :
        1. fetchStart = {pageCount}
    required data searching point :
        header_1 : fixed
        body_1 : pageCount
'''
'''
    @post info

    method : get
    url : 'postUrl'
    header :
        None
'''
class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        print(self.channelCode)

    def get_post_body_post_list_page(self, num=1):
        data = {
            "fetchStart" : num
        }
        return data
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        
        self.pageCount = 1
        while True :
            self.post_list_scraping()
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else:
                break

    def post_list_scraping(self):
        data = {
            "fetchStart" : self.pageCount
        }
        super().post_list_scraping(postListParsingProcess, 'post', data)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess)
    



            

 

