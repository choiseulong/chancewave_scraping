from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 국토교통부

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  http://www.molit.go.kr/USR/BORD0201/m_69/LST.jsp?id=N01_B&desc=asc&lcmspage={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.molit.go.kr/USR/BORD0201/m_69/DTL.jsp?id=N01_B&cate=&mode=view&idx={postId}
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '국토교통부'
        self.postBoardName = '공지사항'
        self.channelMainUrl = 'http://www.molit.go.kr'
        self.postUrl = 'http://www.molit.go.kr/USR/BORD0201/m_69/DTL.jsp?id=N01_B&cate=&mode=view&idx={}'
        
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