from pymongo import MongoClient
from bson.objectid import ObjectId
from .tools import *
from datetime import datetime

class MongoServer:
    def __init__(self):
        self.url = 'mongodb://admin:mysterico@k8s.mysterico.com:31489'
        self.connection = MongoClient(self.url)
        self.db = self.connection.get_database('chancewave_scraper')
        self.collection = self.db.get_collection('scrapingData')
    
    def fine_one(self, query):
        return self.collection.find_one(query)
    
    def find(self, query={}):
        cursor = self.collection.find(query)
        return [i for i in cursor]
    
    def delete_and_insert(self, targetQuery, newData):
        self.collection.remove(targetQuery)
        self.collection.insert_one(newData)
    
    def insert_many(self, data):
        result = self.collection.insert_many(data)
        return result
    
    def update_one(self, target_query, update_query) : 
        self.collection.update_one(target_query, update_query)
    
    def remove_channel_data(self, channelCode):
        self.collection.remove({'channelCode' : channelCode})
    
    def reflect_scraped_data(self, collectedDataList):
        bulkInsertDataList = []
        for newData in collectedDataList:
            postUrl = newData['postUrl']
            crc32 = make_crc(newData)
            newData['crc'] = crc32
            beforeData = self.fine_one({'postUrl' : postUrl})
            if beforeData and postUrl != None :
                if beforeData['crc'] == newData['crc']:
                    if beforeData['isUpdate']:
                        postUrl = beforeData['postUrl']
                        self.update_isUpdate_to_False(postUrl)
                    continue
                elif beforeData['crc'] - newData['crc']:
                    print(beforeData['crc'], newData['crc'])
                    print(f'{postUrl}\n@@ 문서 업데이트 @@')
                    self.update_data_process(newData, beforeData)
            else :
                bulkInsertDataList.append(newData)
        if bulkInsertDataList:
            self.insert_many(bulkInsertDataList)

    def update_data_process(self, newData, beforeData):
        now = datetime.now(timezone('Asia/Seoul')).isoformat()
        newData['isUpdate'] = not newData['isUpdate']
        newData['updatedTime'] = now
        beforeDocId = beforeData['_id']
        targetQuery = {'_id' : beforeDocId}
        self.delete_and_insert(targetQuery, newData)
    
    def update_isUpdate_to_False(self, postUrl):
        target_query = {'postUrl' : postUrl}
        update_query= {'$set' : {'isUpdate' : False}}
        self.update_one(target_query, update_query)






