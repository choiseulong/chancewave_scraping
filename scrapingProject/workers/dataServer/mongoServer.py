from pymongo import MongoClient
from bson.objectid import ObjectId
from .tools import *

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
    
    def insert_many(self, data):
        result = self.collection.insert_many(data)
        return result
    
    def reflect_scraped_data(self, collectedDataList):
        bulkInsertDataList = []
        for data in collectedDataList:
            contentsUrl = data['contentsUrl']
            doc = self.fine_one({'contentsUrl' : contentsUrl})
            if doc :
                self.update_data_process(doc)
            else :
                bulkInsertDataList.append(data)
        if bulkInsertDataList:
            self.insert_many(bulkInsertDataList)

    def update_data_process(self, doc):
        pass






