from workers.dataScraper.parser.seoul_woman_up import *
from workers.dataScraper.scraper.topLevelScrper import Scraper as ABCScraper

'''
    0,1,2 required
    User-Agent = ''
'''

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://www.seoulwomanup.or.kr/womanup/common/bbs/selectBBS.do?bbs_seq={}&bbs_code=noticeall'

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
        super().post_list_scraping(postListParsingProcess, 'get')

    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess)