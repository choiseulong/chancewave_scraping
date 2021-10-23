from pymongo import MongoClient
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
    
    def total_document_count(self):
        return self.collection.count()
    
    def insert_new_target_channel(self, target):
        channelName = target.channelName
        channelUrl = target.channelUrl
        self.connection_mongodb()
        self.set_collection('scrapingHistory')
        count = self.total_document_count()
        channelDataFrame = get_channel_data_frame(channelName, channelUrl, count)
        self.collection.insert(channelDataFrame)
    

