from pymongo.errors import *
from pymongo import MongoClient
from .tools import *
from datetime import datetime
from time import sleep
from pytz import timezone

class MongoServer:

    def __init__(self, dev):
        if dev == True:
            print('dev mongodb')
            # self.url = 'mongodb://admin:mysterico@k8s.mysterico.com:31489'
            self.url = 'mongodb://CHANCEWAVE:MYSTERICO@127.0.0.1:9202' # local mongo containier
            self.connection = MongoClient(self.url)
            self.db = self.connection.get_database('scraping')
            self.collection = self.db.get_collection('data')
        elif dev == False :
            # self.url = 'mongodb://CHANCEWAVE:MYSTERICO@mongodb_container:27017/'
            self.url = 'mongodb://CHANCEWAVE:MYSTERICO@211.42.153.221:9202' # ubuntu url
            self.connection = MongoClient(self.url)
            self.db = self.connection.get_database('scraping')
            self.collection = self.db.get_collection('data')

    def fine_one(self, query):
        return self.collection.find_one(query)
    
    def find(self, query={}, projection={}, count=0):
        if count :
            cursor = self.collection.find(query, projection).limit(count)
        else:
            cursor = self.collection.find(query, projection)
        return [i for i in cursor]

    def find_paging(self, query={}, projection={}, count=0, page=1):
        cursor = self.collection.find(query, projection).limit(count).skip(count * (page-1))
        return [i for i in cursor]
    
    def delete_and_insert(self, target_query, new_data):
        self.collection.remove(target_query)
        self.collection.insert_one(new_data)
    
    def insert_many(self, data):
        result = self.collection.insert_many(data)
        return result
    
    def update_one(self, target_query, update_query) : 
        self.collection.update_one(target_query, update_query)
    
    def remove_channel_data(self, channel_code):
        self.collection.remove({'channel_code' : channel_code})
    
    def reflect_scraped_data(self, collected_data_list):
        bulk_insert_data_list = []
        for new_data in collected_data_list:
            post_url = new_data['post_url']
            channel_code = new_data['channel_code']
            crc32 = make_crc(new_data)
            new_data['crc'] = crc32
            before_data = self.fine_one({'post_url' : post_url, "channel_code" : channel_code})
            if before_data and post_url != None :
                if before_data['crc'] == new_data['crc']:
                    post_url = before_data['post_url']
                    self.update_checkTime(post_url, before_data)
                    continue
                elif before_data['crc'] - new_data['crc']:
                    self.update_data_process(new_data, before_data)
            else :
                bulk_insert_data_list.append(new_data)
        if bulk_insert_data_list:
            self.insert_many(bulk_insert_data_list)

    def update_data_process(self, new_data, before_data):
        now = datetime.now(timezone('Asia/Seoul')).isoformat()
        is_update_check = before_data['is_update_check_time']
        is_update_check.append(now)
        updated_time = before_data['updated_time']
        updated_time.append(now)
        new_data['created_time'] = before_data['created_time']
        new_data['is_update_check_time'] = is_update_check
        new_data['updated_time'] = updated_time
        before_doc_id = before_data['_id']
        target_query = {'_id' : before_doc_id}
        self.delete_and_insert(target_query, new_data)
    
    def update_checkTime(self, post_url, before_data):
        now = datetime.now(timezone('Asia/Seoul')).isoformat()
        is_update_check = before_data['is_update_check_time']
        is_update_check.append(now)
        target_query = {'post_url' : post_url}
        update_query= {'$set' : {'is_update_check_time' : is_update_check}}
        self.update_one(target_query, update_query)

    def get_data(self, channel_code, count=0, page=0):
        query = {"channel_code" : channel_code}
        projection = {'_id' : 0}
        if page :
            data = self.find_paging(query, projection, count, page)
        else:
            data = self.find(query, projection, count)
        return data

    def get_total_data(self):
        query = {}
        projection = {'_id': 0}
        data = self.find(query, projection)
        return data

    def write_scraping_history(self, data):
        collection = self.db.get_collection('history')
        collection.insert_one(data)




