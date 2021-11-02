from workers.dataServer.mongoServer import MongoServer
from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
from workers.dataScraper.parser.seoul_forever_educateion_portal import *
import json

'''
    postListUrl -

    method = POST
    body = {
        "rows" : 999999,
        "board_no" : "14"
    }
    Content-Type: application/x-www-form-urlencoded
    Cookie : 


    contents
    method = POST
    body = {
        "boarditem_no" : item_no,
        "board_no" : 14,
        "attach_file_use_yn" : file_use
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
        self.postListUrl = 'https://sll.seoul.go.kr/lms/front/boardItem/doListView.dunet'
        self.postUrl = 'https://sll.seoul.go.kr/lms/front/boardItem/doViewBoardItem.dunet'
        self.additionalKeyValue = []
    
    def set_headers_process(self, channelUrl):
        status, response = get_method_response(self.session, channelUrl)
        if status == 'ok':
            JSESSIONID =  extract_jsessionid_from_response_header(response.headers)
            self.additionalKeyValue.append(['Cookie', f'JSESSIONID={JSESSIONID};'])
            self.additionalKeyValue.append(['Content-Type', 'application/x-www-form-urlencoded'])
            self.session = set_headers(self.session, self.additionalKeyValue)
        

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        self.set_headers_process(channelUrl)
        self.post_list_scraping(channelCode)
        if self.scrapingTarget :
            self.target_contents_scraping()
            self.collect_data(channelCode, channelUrl)
            self.mongo.reflect_scraped_data(self.collectedDataList)

    def post_list_scraping(self, channelCode):
        data = {
            "rows" : 999999,
            "board_no" : "14"
        }
        status, response = post_method_response(self.session, self.postListUrl, data)
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

