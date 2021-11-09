from workers.dataScraper.parser.seoul_woman_up import *
from workers.dataScraper.scraper.topLevelScrper import Scraper as ABCScraper

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)

    def scraping_process(self, channelCode, channelUrl, dateRange):
        print(channelCode)
        super().scraping_process(channelCode, channelUrl, dateRange)

        if '0' in self.channelCode: 
            self.postUrl = 'https://www.seoulwomanup.or.kr/womanup/common/bbs/selectBBS.do?bbs_seq={}&bbs_code=noticeall'
        elif '1' in self.channelCode: 
            self.postUrl = 'https://www.seoulwomanup.or.kr/womanup/common/bbs/selectBBS.do?bbs_seq={}&bbs_code=centerall'
        elif '2' in self.channelCode: 
            self.mongo.remove_channel_data(channelCode)
            
        self.session = set_headers(self.session)
        self.pageCount = 1
        while True :
            self.channelUrl = self.channelUrlFrame.format(self.pageCount)
            self.post_list_scraping()
            if self.scrapingTarget :
                if '2' not in self.channelCode:
                    self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collectedDataList)
                self.pageCount += 1
            else :
                print(self.channelCode, "empty point")
                break

    def post_list_scraping(self):
        if '2' not in self.channelCode: 
            super().post_list_scraping(postListParsingProcess, 'get')
        else :
            super().post_list_scraping(postContentParsingProcess_second, 'get')


    def target_contents_scraping(self):
        super().target_contents_scraping(postContentParsingProcess)
    