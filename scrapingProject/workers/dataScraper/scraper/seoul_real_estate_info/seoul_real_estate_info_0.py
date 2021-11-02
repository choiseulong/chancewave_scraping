from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
from workers.dataScraper.parser.seoul_real_estate_info import *
from workers.dataServer.mongoServer import MongoServer

'''
    method = POST
    body =  {
        'page' : num
    }

'''

class Scraper:
    def __init__(self, session):
        self.scrapingTarget = []
        self.scrapingTargetContents = []
        self.collectedDataList = []
        self.session = session
        self.dateRange = []
        self.mongo = ''

    def get_post_body_post_list_page(self, num=1):
        data = {
            "page" : num
        }
        return data
    
    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        pageCount = 1
        while True :
            self.post_list_scraping(channelCode, pageCount, channelUrl)
            if self.scrapingTarget:
                self.target_contents_scraping()
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else :
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
                break
    
    def post_list_scraping(self, channelCode, pageCount, channelUrl):
        data = self.get_post_body_post_list_page(pageCount)
        status, response = post_method_response(self.session, channelUrl, data)
        if status == 'ok' :
            self.scrapingTarget = extract_post_list_from_response_text(response.json(), self.dateRange, channelCode)
        else :
            raise Exception(f'scraping channel {channelCode} post list error')  
    
    def target_contents_scraping(self):
        scrapingTargetContents = []
        for target in self.scrapingTarget :
            url = target['postUrl']
            status, response = get_method_response(self.session, url)
            if status == 'ok':
                contentsResult = extract_post_contents_from_response_text(response.text)
                scrapingTargetContents.append(contentsResult)
        self.scrapingTargetContents = scrapingTargetContents
    
    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for postList, contents in zip(self.scrapingTarget, self.scrapingTargetContents):
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrameWithPostList, contents)
            collectedDataList.append(dataFrameWithContents)
        self.collectedDataList = collectedDataList