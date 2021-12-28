from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 경기도청

# 타겟 : 분야별 소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.gg.go.kr/bbs/board.do?bsIdx=570&menuId=1590#page={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gg.go.kr/bbs/boardView.do?bIdx={postId}&bsIdx=570&bcIdx=0&menuId=1590&isManager=false&isCharge=false&page=1
    header :
        None

'''
sleepSec = 2
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channelName = '경기도청'
        self.postBoardName = '분야별 소식'
        self.channelMainUrl = 'https://www.gg.go.kr/'
        self.postUrl = 'https://www.gg.go.kr/bbs/boardView.do?bIdx={}&bsIdx=570&bcIdx=0&menuId=1590&isManager=false&isCharge=false&page=1'

    def scraping_process(self, channelCode, channelUrl, dateRange):
        super().scraping_process(channelCode, channelUrl, dateRange)
        self.session = set_headers(self.session)
        self.pageCount = 0
        while True:
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            list_param = {
                'bsIdx': 570,
                'bcIdx': 0,
                'menuId': 1590,
                'isManager': 'false',
                'isCharge': 'false',
                'offset': self.pageCount * 10,
                'limit': 10
            }

            self.channelUrl = 'https://www.gg.go.kr/ajax/board/getList.do'

            self.post_list_scraping(postListParsingProcess, 'post', data=list_param, jsonize=False)
            if self.scrapingTarget:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else:
                break

    # def post_list_scraping(self):
    #     super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess, sleepSec)