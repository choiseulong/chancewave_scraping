from workers.dataScraper.scraper.topLevelScrper import Scraper as ABCScraper
from workers.dataScraper.parser.seoul_city import *
from workers.dataScraper.scraperTools.tools import *

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
                self.collect_data(channelCode, channelUrl)
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
    



            

 

