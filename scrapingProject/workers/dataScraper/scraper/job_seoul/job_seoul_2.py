from workers.dataScraper.parser.job_seoul import *
from workers.dataServer.mongoServer import MongoServer
from .job_seoul_0 import Scraper as job_seoul_0_Scraper
import json

'''
    target post list 
    User-Agent: ''

    target post contents
    Cookie: JSESSIONID_1=80nfaCx1xlYAto1vYB0WIcl7glKYVBdf5dIXAaSp5AlDPX3RpenUEDjA01kGKHHy.sjpc_was2_servlet_engine1

    where?
    form 태그 attrs name = "rEdcLst" 에서 action attrs 속에 있음
    jsessionid= 와
    ?method 사이
    <form name="rEdcLst"  method="post" action="/www/training/center_training/Www_center_edc.do;jsessionid=80nfaCx1xlYAto1vYB0WIcl7glKYVBdf5dIXAaSp5AlDPX3RpenUEDjA01kGKHHy.sjpc_was2_servlet_engine1?method=getWww_center_edc">
'''

class Scraper(job_seoul_0_Scraper):
    def __init__(self, session):
        super().__init__(session)
        self.postUrl = 'https://job.seoul.go.kr/www/training/center_training'
        # ./Www~~ 형식으로 postUrl 이 들어오니 [1:] 부터 기존에 url 에 붙여서 사용하면 될듯
        self.additinalHeaderElement = []
        self.extract_post_list_from_response_text = other_extract_post_list_from_response_text
        self.extract_post_contents_from_response_text = other_extract_post_contents_from_response_text

    def target_contents_scraping(self):
        scrapingTargetContents = []
        self.additinalHeaderElement.append(['Cookie', 'JSESSIONID_1='+self.scrapingTarget[-1]])
        self.set_headers(self.additinalHeaderElement)
        del self.scrapingTarget[-1]
        for target in self.scrapingTarget :
            postUrl = target['postUrl']
            postUrl = self.postUrl + postUrl
            status, response = get_method_response(self.session, postUrl)
            if status == 'ok':
                TargetContents = self.extract_post_contents_from_response_text(response.text)
                scrapingTargetContents.append(TargetContents)
        self.scrapingTargetContents = scrapingTargetContents

    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for postList, contents in zip(self.scrapingTarget, self.scrapingTargetContents):
            postList['postUrl'] = self.postUrl + postList['postUrl'] 
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrameWithPostList, contents)
            collectedDataList.append(dataFrameWithContents)
        self.collectedDataList = collectedDataList