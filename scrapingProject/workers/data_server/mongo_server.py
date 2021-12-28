from pymongo.errors import *
from pymongo import MongoClient
from .tools import *
from datetime import datetime
import traceback

class mongo_server:
    def __init__(self):
        self.url = 'mongodb://admin:mysterico@k8s.mysterico.com:31489'
        # self.url = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/'
        self.connection = MongoClient(self.url)
        self.db = self.connection.get_database('scraping')
        self.collection = self.db.get_collection('data')

    
    def fine_one(self, query):
        return self.collection.find_one(query)
    
    def find(self, query={}, projection={}):
        cursor = self.collection.find(query, projection)
        return [i for i in cursor]
    
    def delete_and_insert(self, targetQuery, newData):
        self.collection.remove(targetQuery)
        self.collection.insert_one(newData)
    
    def insert_many(self, data):
        result = self.collection.insert_many(data)
        return result
    
    def update_one(self, target_query, update_query) : 
        self.collection.update_one(target_query, update_query)
    
    def remove_channel_data(self, channel_code):
        self.collection.remove({'channel_code' : channel_code})
    
    def reflect_scraped_data(self, collected_data_list):
        bulkInsertDataList = []
        for newData in collected_data_list:
            post_url = newData['post_url']
            channel_code = newData['channel_code']
            crc32 = make_crc(newData)
            newData['crc'] = crc32
            beforeData = self.fine_one({'post_url' : post_url, "channel_code" : channel_code})
            if beforeData and post_url != None :
                if beforeData['crc'] == newData['crc']:
                    post_url = beforeData['post_url']
                    self.update_checkTime(post_url, beforeData)
                    continue
                elif beforeData['crc'] - newData['crc']:
                    # print(f'{post_url}\n@@ 문서 업데이트 @@')
                    self.update_data_process(newData, beforeData)
            else :
                bulkInsertDataList.append(newData)
        if bulkInsertDataList:
            self.insert_many(bulkInsertDataList)

    def update_data_process(self, newData, beforeData):
        now = datetime.now(timezone('Asia/Seoul')).isoformat()
        isUpdateCheck = beforeData['is_update_check_time		']
        isUpdateCheck.append(now)
        updated_time = beforeData['updated_time']
        updated_time.append(now)
        newData['is_update_check_time		'] = isUpdateCheck
        newData['updated_time'] = updated_time
        beforeDocId = beforeData['_id']
        targetQuery = {'_id' : beforeDocId}
        self.delete_and_insert(targetQuery, newData)
    
    def update_checkTime(self, post_url, beforeData):
        now = datetime.now(timezone('Asia/Seoul')).isoformat()
        isUpdateCheck = beforeData['is_update_check_time		']
        isUpdateCheck.append(now)
        target_query = {'post_url' : post_url}
        update_query= {'$set' : {'is_update_check_time		' : isUpdateCheck}}
        self.update_one(target_query, update_query)

    def get_data(self, channel_code):
        query = {"channel_code" : channel_code}
        projection = {'_id': 0}
        data = self.find(query, projection)
        return data

    def get_total_data(self):
        query = {}
        projection = {'_id': 0}
        data = self.find(query, projection)
        return data






