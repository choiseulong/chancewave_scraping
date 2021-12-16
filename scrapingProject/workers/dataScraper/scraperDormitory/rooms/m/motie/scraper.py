from workers.dataScraper.scraperDormitory.scraping_default_usage import Scraper as ABCScraper
from workers.dataScraper.scraperDormitory.scraperTools.tools import *
from .parser import *

# 채널 이름 : 산업통상자원부
# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시
#HTTP Request
'''
    @post list

    method : GET
    url =  http://www.motie.go.kr/motie/ne/Notice/bbs/bbsList.do?bbs_cd_n=83&bbs_seq_n=&currentPage={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.motie.go.kr/motie/ne/Notice/bbs/bbsView.do?bbs_seq_n={postId}&bbs_cd_n=83
    header :
        None

'''
sleepSec = 2
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelMainUrl = 'http://www.motie.go.kr'
        self.postUrl = 'http://www.motie.go.kr/motie/ne/Notice/bbs/bbsView.do?bbs_seq_n={}&bbs_cd_n=83'

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