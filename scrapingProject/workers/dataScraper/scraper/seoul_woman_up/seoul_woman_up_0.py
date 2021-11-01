from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parser.seoul_woman_up import *
from workers.dataServer.mongoServer import MongoServer

'''
    0,1,2 required
    User-Agent = ''
'''

class Scraper:
    def __init__(self, session):
        self.session = session
        self.dateRange = []
        self.mongo = ''
        self.scrapingTarget = []
        self.scrapingTargetContents = []
        self.collectedDataList = []
        self.postUrl = 'https://www.seoulwomanup.or.kr/womanup/common/bbs/selectBBS.do?bbs_seq={}&bbs_code=noticeall'
        self.channelMainUrl = 'https://www.seoulwomanup.or.kr'

        # function
        self.extract_post_list_from_response_text = extract_post_list_from_response_text
        self.extract_post_contents_from_response_text = extract_post_contents_from_response_text

    def scraping_process(self, channelCode, channelUrl, dateRange):
        self.mongo = MongoServer()
        self.dateRange = dateRange
        self.session = set_headers(self.session)
        pageCount = 1
        while True :
            channelUrlWithPageCount = channelUrl.format(pageCount)
            self.post_list_scraping(channelCode, channelUrlWithPageCount)
            if self.scrapingTarget :
                self.target_contents_scraping()
                self.collect_data(channelCode, channelUrlWithPageCount)
                self.mongo.reflect_scraped_data(self.collectedDataList)
                pageCount += 1
            else:
                print(f'{channelCode}, 유효한 포스트 미존재 지점에 도달하여 스크래핑을 종료합니다')
                break

    def post_list_scraping(self, channelCode, channelUrl):
        status, response = get_method_response(self.session, channelUrl)
        if status == 'ok':
            self.scrapingTarget = self.extract_post_list_from_response_text(response.text, self.dateRange, channelCode, self.postUrl)
        else :
            raise Exception(f'scraping channel {channelCode} post list error')

    def target_contents_scraping(self):
        scrapingTargetContents = []
        for target in self.scrapingTarget :
            postUrl = target['postUrl']
            status, response = get_method_response(self.session, postUrl)
            if status == 'ok':
                targetContents = self.extract_post_contents_from_response_text(response.text, self.channelMainUrl)
                scrapingTargetContents.append(targetContents)
        self.scrapingTargetContents = scrapingTargetContents
           
    def collect_data(self, channelCode, channelUrl):
        collectedDataList = []
        for postList, contents in zip(self.scrapingTarget, self.scrapingTargetContents):
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrameWithPostList, contents)
            collectedDataList.append(dataFrameWithContents)
        self.collectedDataList = collectedDataList