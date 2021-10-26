from ..scraperTools.tools import *
from ..parser.channel_a import * 
from workers.dataServer.mongoServer import MongoServer

'''
    required :
        headers :
            User-Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36
        body : 
            {"fetchStart" : Number}
'''
class Scraper:
    def __init__(self):
        self.headers = ''
        self.postListResult = []
        self.contentsResultList = []
    
    def get_headers(self):
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        return headers
    
    def get_post_body_post_list_page(self, num=1):
        data = {
            "fetchStart" : num
        }
        return data

    def scraping_process(self, session, channelCode, channelUrl):
        mongo = MongoServer()
        mongo.connection_mongodb()
        mongo.set_collection(channelCode)
        session.headers = self.get_headers()
        totalPageCount = 0
        pageCount = 1

        while True :
            self.postListResult = self.search_post_list(pageCount, session, channelUrl)
            contentsUrl = self.postListResult['contentsUrl']
            if not totalPageCount :
                totalPageCount = search_total_post_count(self.postListResult[0])
            self.contentsResultList = self.search_post_contents(session, self.postListResult)
            if pageCount > totalPageCount :
                break
            else :
                collectedDataList = self.collect_data(channelCode, channelUrl)
                insert_result = mongo.insert_many(collectedDataList)
                print(insert_result, channelCode)
                # print(collectedDataList)
                pageCount += 1
            break
    
    def search_post_list(self, pageCount, session, channelUrl):
        data = self.get_post_body_post_list_page(pageCount)
        status, response = post_method_response(session, channelUrl, {}, data)
        if status == 'ok' :
            result = extract_post_list_from_response_text(response.text)
            return result
        else :
            raise Exception('scraping channel a1 post list error')

    def search_post_contents(self, session, postListResult):
        contentsResultList = []
        for postData in postListResult :
            url = postData['contentsUrl']
            status, response = get_method_response(session, url)
            if status == 'ok':
                contentsResult = extract_post_contents_from_response_text(response.text)
                contentsResultList.append(contentsResult)
        return contentsResultList
    
    def collect_data(self, channelCode, channelUrl):
        dataList = []
        for postList, contents in zip(self.postListResult, self.contentsResultList):
            dataFrame = get_post_data_frame(channelCode, channelUrl)
            dataFrameWithPostList = enter_data_into_dataFrame(dataFrame, postList)
            dataFrameWithContents = enter_data_into_dataFrame(dataFrameWithPostList, contents)
            dataList.append(dataFrameWithContents)
        return dataList


            

 

