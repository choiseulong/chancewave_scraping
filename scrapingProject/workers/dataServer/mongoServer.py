from pymongo import MongoClient
from bson.objectid import ObjectId
from .tools import *

class MongoServer:
    def __init__(self):
        self.db = ''
        self.collection = ''
    
    def connection_mongodb(self):
        url = 'mongodb://admin:mysterico@k8s.mysterico.com:31489'
        connection = MongoClient(url)
        self.db = connection.get_database('data_voucher')
    
    def set_collection(self, collection_name):
        self.collection = self.db.get_collection(collection_name)
    
    def fine_one(self, query):
        return self.collection.find_one(query)

    def total_document_count(self):
        return self.collection.count()
    
    def find(self, query={}):
        cursor = self.collection.find(query)
        return [i for i in cursor]
    
    def insert_new_target_channel(self, target):
        self.connection_mongodb()
        self.set_collection('scrapingHistory')
        channelName = target.channelName
        channelUrl = target.channelUrl
        data = self.fine_one({'channelName' : channelName})
        if not data:
            count = self.total_document_count()
            channelDataFrame = get_channel_data_frame(channelName, channelUrl, count)
            insert_result = self.collection.insert(channelDataFrame)
            if ObjectId == type(insert_result):
                return f'success init, target : {channelName}'
            else :
                return f'fail init, target : {channelName}'
        if data:
            raise Exception('이미 존재하는 채널입니다.')
    
    def serve_channel_data(self):
        self.connection_mongodb()
        self.set_collection('scrapingHistory')
        dataList = self.find()
        return dataList



