from workers.dataScraper.parser.seoul_woman_up import *
from .seoul_woman_up_0 import Scraper as default_scraper

class Scraper(default_scraper):
    def __init__(self, session):
        super().__init__(session)
        self.extract_post_contents_from_response_text = extract_post_contents_from_response_text_other

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.mongo.remove_channel_data(channelCode)
        self.dateRange = dateRange
        self.session = set_headers(self.session)
        pageCount = 1
        while True :
            channelUrlWithPageCount = channelUrl.format(pageCount)
            self.target_contents_scraping(channelUrlWithPageCount)
            if self.scrapingTargetContents :
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else:
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
            break

    def target_contents_scraping(self, channelUrlWithPageCount):
        status, response = get_method_response(self.session, channelUrlWithPageCount)
        if status == 'ok':
            self.scrapingTargetContents = self.extract_post_contents_from_response_text(response.text, self.dateRange)
    
    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for contents in self.scrapingTargetContents:
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrame, contents)
            collectedDataList.append(dataFrameWithContents)
        self.collectedDataList = collectedDataList
        
        