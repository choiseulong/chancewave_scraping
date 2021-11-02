from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
from workers.dataScraper.parser.seoul_welfare_portal import *
from workers.dataServer.mongoServer import MongoServer
'''

'''
class Scraper:
    def __init__(self, session):
        self.scrapingTarget = []
        self.scrapingTargetContents = []
        self.collectedDataList = []
        self.session = session
        self.dateRange = []
        self.mongo = ''

        self.extract_post_list_from_response_text = extract_post_list_from_response_text

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        pageCount = 1
        while True :
            channelUrlWithPageCount = channelUrl.format(pageCount)
            self.post_list_scraping(channelCode, channelUrlWithPageCount)
            if self.scrapingTarget :
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else :
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
                break
    
    def post_list_scraping(self, channelCode, channelUrlWithPageCount):
        status, response = get_method_response(self.session, channelUrlWithPageCount)
        if status == 'ok':
            self.scrapingTarget = self.extract_post_list_from_response_text(response.content, self.dateRange, channelCode)
        else :
            raise Exception(f'scraping channel {channelCode} post list error')

    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for postList in self.scrapingTarget:
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            collectedDataList.append(dataFrameWithPostList)
        self.collectedDataList = collectedDataList
    