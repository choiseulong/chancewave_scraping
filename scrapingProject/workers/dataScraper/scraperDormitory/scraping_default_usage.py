from workers.dataServer.mongoServer import MongoServer
from .scraperTools.tools import *
from .parserTools.tools import * 
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
        self.emptyPageCount = 0
        self.additionalKeyValue = []
        self.retryCount = 0

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

    def post_list_scraping(self, postListParsingProcess, method, data='', sleepSec=2):
        '''
            채널 메인에서 게시글의 기본정보를 가져오기 위한 요청을 처리함
        '''
        if method == 'get':
            status, response = get_method_response(self.session, self.channelUrl, sleepSec)
        elif method == 'post':
            status, response = post_method_response(self.session, self.channelUrl, data, sleepSec)

        if status == 'ok':
            self.scrapingTarget = postListParsingProcess(
                response = response, 
                dateRange = self.dateRange, 
                channelCode = self.channelCode, 
                postUrlFrame = self.postUrl,
                pageCount = self.pageCount,
                channelMainUrl = self.channelMainUrl
            )

    def target_contents_scraping(self, postContentParsingProcess, sleepSec=2):
        '''
            채널 상세정보 수집을 위해 추가 요청이 필요한 경우 작성함
        '''
        data = {}
        postUrl = ''
        for target in self.scrapingTarget :
            postContent = self.target_try(postContentParsingProcess, target, sleepSec)
            if postContent:
                self.scrapingTargetContents.append(postContent)

    def target_try(self, postContentParsingProcess, target, sleepSec):
        if 'postUrl' in target.keys():
            postUrl = target['postUrl']
            status, response = get_method_response(self.session, postUrl, sleepSec)
        elif 'contentsReqParams' in target.keys():
            data = target['contentsReqParams']
            status, response = post_method_response(self.session, self.postUrl, data, sleepSec)

        if status == 'ok':
            postContent = postContentParsingProcess(
                response = response, 
                channelUrl = self.channelUrl,
                postUrlFrame = self.postUrl,
                channelMainUrl = self.channelMainUrl
            )
            if postContent == 'retry' : 
                sleep(300)
                print(f'{self.channelCode} - retry : {self.retryCount}')
                self.retryCount += 1
                if self.retryCount == 3:
                    self.retryCount = 0
                    postContent = []
                else :
                    postContent = self.target_try(postContentParsingProcess, target, sleepSec)
            return postContent




        



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
                postUrlCanUse = False
            else :
                postUrlCanUse = True
            dataFrame = get_post_data_frame(self.channelCode, self.channelUrl, postUrlCanUse)
            dataFrameWithTargetInfo = enter_data_into_dataFrame(dataFrame, targetInfo)
            dataFrameWithTargetContents = enter_data_into_dataFrame(dataFrameWithTargetInfo, targetContents)
            self.collectedDataList.append(dataFrameWithTargetContents)
        self.scrapingTargetContents = []
        self.scrapingTarget = []