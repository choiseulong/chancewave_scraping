from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 진주시청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.jinju.go.kr/00130/02730/00136.web?extParam=notice&gcode=2144&cpage={pageCount}
    header :
        None


'''
'''
    @post info
    method : GET
    url : https://www.jinju.go.kr/00130/02730/00136.web?gcode=4118&idx={postId}&amode=view&extParam=notice
    header :
        None

'''
sleepSec = 10
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '진주시청'
        self.postBoardName = '새소식'
        self.channelMainUrl = 'https://www.jinju.go.kr'
        self.postUrl = 'https://www.jinju.go.kr/00130/02730/00136.web?gcode=4118&idx={}&amode=view&extParam=notice'
        
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
        super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)