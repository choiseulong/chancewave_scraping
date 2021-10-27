from workers.dataScraper.parser.job_seoul import *
from workers.dataServer.mongoServer import MongoServer
import json

'''
    required in headers
    User-Agent: ''
'''


class Scraper:
    def __init__(self, session):
        self.session = session
        self.dateRange = []
        self.mongo = ''
        self.scrapingTarget = []
        self.scrapingTargetContents = []
        self.collectedDataList = []
        self.contentsUrl = 'https://job.seoul.go.kr/www/custmr_cntr/ntce/WwwNotice.do?method=getWwwNotice&noticeCmmnSeNo=1'
    
    def set_headers(self, additionalKeyValue=None):
        headers = {
            "User-Agent" : ""
        }
        if additionalKeyValue :
            for keyValue in additionalKeyValue:
                key = keyValue[0]
                value = keyValue[1]

                headers.update({key:value})
        self.session.headers = headers
        return headers

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        pageCount = 1

        while True :
            self.set_headers()
            channelUrlWithPageCount = channelUrl.format(pageCount)
            self.post_list_scraping(channelCode, channelUrlWithPageCount)
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data(channelCode, channelUrl)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else :
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
                break
    
    def post_list_scraping(self, channelCode, channelUrl):
        status, response = get_method_response(self.session, channelUrl)
        if status == 'ok':
            self.scrapingTarget = extract_post_list_from_response_text(response.text, self.dateRange, channelCode)
        else :
            raise Exception(f'scraping channel {channelCode} post list error')
        
    def target_contents_scraping(self):
        scrapingTargetContents = []
        for target in self.scrapingTarget :
            data = target['contentsReqParams']
            dummpyHeaders = {}
            self.set_headers([['Content-Type', 'application/x-www-form-urlencoded']])
            status, response = post_method_response(self.session, self.contentsUrl, dummpyHeaders, data)
            if status == 'ok':
                targetContents = extract_post_contents_from_response_text(response.text)
                scrapingTargetContents.append(targetContents)
        self.scrapingTargetContents = scrapingTargetContents
           
    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for postList, contents in zip(self.scrapingTarget, self.scrapingTargetContents):
            reqBody = postList['contentsReqParams']
            del postList['contentsReqParams']
            postList.update({'contentsUrl': self.contentsUrl + json.dumps(reqBody)}) 
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrameWithPostList, contents)
            collectedDataList.append(dataFrameWithContents)
        self.collectedDataList = collectedDataList