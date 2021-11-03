from workers.dataServer.mongoServer import MongoServer
from workers.dataScraper.scraperTools.tools import *
# from workers.dataScraper.parserTools.tools import * 
from workers.dataScraper.parser.seoul_housing_portal import *

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
        self.postListUrl = 'https://sll.seoul.go.kr/lms/front/boardItem/doListView.dunet'
        self.postUrl = 'https://sll.seoul.go.kr/lms/front/boardItem/doViewBoardItem.dunet'
        self.additionalKeyValue = []

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        pageCount = 1
        while True:
            channelUrlWithPageCount = channelUrl.format(pageCount)
            self.post_list_scraping(channelCode, channelUrlWithPageCount)
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else :
                break

    def post_list_scraping(self, channelCode, channelUrlWithPageCount):
        status, response = get_method_response(self.session, channelUrlWithPageCount)
        if status == 'ok':
            self.scrapingTarget = extract_post_list_from_response_text(response.text, self.dateRange, channelCode)
        else :
            raise Exception(f'scraping channel {channelCode} post list error')
    
    def target_contents_scraping(self):
        scrapingTargetContents = []
        for target in self.scrapingTarget :
            data = target['contentsReqParams']
            status, response = post_method_response(self.session, self.postUrl, data)
            if status == 'ok':
                targetContents = extract_post_contents_from_response_text(response.text)
                scrapingTargetContents.append(targetContents)
        self.scrapingTargetContents = scrapingTargetContents
    
    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for postList, contents in zip(self.scrapingTarget, self.scrapingTargetContents):
            reqBody = postList['contentsReqParams']
            del postList['contentsReqParams']
            postList.update({'postUrl': self.postUrl + json.dumps(reqBody)}) 
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrameWithPostList, contents)
            collectedDataList.append(dataFrameWithContents)
        self.collectedDataList = collectedDataList

