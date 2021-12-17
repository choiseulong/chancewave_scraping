from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기콘텐츠진흥원

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시


#HTTP Request
'''
    @post list

    method : GET
    url = https://www.gcon.or.kr/busiNotice?pageNum={pageCount}&rowCnt={포스트 숫자}&menuId=MENU02369
    header :
        User-Agent
    required data searching point :
        header_1 : fixed
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

sleepSec = 3

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '경기콘텐츠진흥원'
        self.postBoardName = '사업공고'
        self.channelMainUrl = "https://www.gcon.or.kr"
    
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
        if self.channelCode == 'gyeonggi_content_agency_1':
            postContentParsingProcess = postContentParsingProcess_other
            self.postBoardName = '교육 및 행사'

        super().target_contents_scraping(postContentParsingProcess, sleepSec)