from workers.dataServer.mongoServer import MongoServer
from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
import json
from abc import *

class Scraper(metaclass=ABCMeta):
    def __init__(self, session):
        # default var
        self.session = session
        self.dateRange = []
        self.mongo = ''
        self.channelCode = ''
        self.channelUrl = ''
        self.channelUrlFrame = ''
        self.pageCount = 0

        # scraped data
        self.scrapingTarget = []
        self.scrapingTargetContents = []
        self.collectedDataList = []

        # additional urls
        self.postUrl = ''
        self.postListUrl = ''
        self.channelMainUrl = ''

    @abstractmethod
    def scraping_process(self, channelCode, channelUrl, dateRange):
        '''
            스크래핑 진행의 틀을 작성함
        '''
        self.mongo = MongoServer()
        self.dateRange = dateRange
        self.channelCode = channelCode
        self.channelUrl = channelUrl
        self.channelUrlFrame = channelUrl #pageCount 적용이 필요한 경우 사용
        # 추가 로직 작성 必

    def post_list_scraping(self, postListParsingProcess, method, data=''):
        '''
            채널 메인에서 게시글의 기본정보를 가져오기 위한 요청을 처리함
        '''
        if method == 'get':
            status, response = get_method_response(self.session, self.channelUrl)
        elif method == 'post':
            status, response = post_method_response(self.session, self.channelUrl, data)
        self.scrapingTarget = postListParsingProcess(
            response = response, 
            dateRange = self.dateRange, 
            channelCode = self.channelCode, 
            postUrl = self.postUrl
        )

    def target_contents_scraping(self, postContentParsingProcess):
        '''
            채널 상세정보 수집을 위해 추가 요청이 필요한 경우 작성함
        '''
        for target in self.scrapingTarget :
            if 'postUrl' in target.keys():
                postUrl = target['postUrl']
                status, response = get_method_response(self.session, postUrl)
            elif 'contentsReqParams' in target.keys():
                data = target['contentsReqParams']
                status, response = post_method_response(self.session, self.postUrl, data)
            self.scrapingTargetContents.append(
                postContentParsingProcess(
                    response = response, 
                    channelUrl = self.channelUrl
                )
            )

    def collect_data(self):
        '''
            채널 메인에서 게시글의 기본 정보를 담고
            게시글 페이지에서 상세 정보를 담아오면
            이를 DB에 반영하기전 합치는 로직에 해당함
        '''
        if not self.scrapingTargetContents:
            self.scrapingTargetContents = [{} for _ in range(len(self.scrapingTarget))] 
        for targetInfo, targetContents in zip(self.scrapingTarget, self.scrapingTargetContents):
            if 'contentsReqParams' in targetInfo.keys():
                reqBody = targetInfo['contentsReqParams']
                del targetInfo['contentsReqParams']
                targetInfo.update({'postUrl': self.postUrl + json.dumps(reqBody)}) 
            dataFrame = get_post_data_frame(self.channelCode, self.channelUrl)
            dataFrameWithTargetInfo = enter_data_into_dataFrame(dataFrame, targetInfo)
            dataFrameWithTargetContents = enter_data_into_dataFrame(dataFrameWithTargetInfo, targetContents)
            self.collectedDataList.append(dataFrameWithTargetContents)


    def set_headers_process(self):
        '''
            session headers 에 cookie, content-type 등 추가 params가 필요한 경우에 작성함
        '''
        pass
