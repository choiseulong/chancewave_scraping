from pymongo import MongoClient

class MongoServer:
    def __init__(self):
        self.url = ''
        self.connection = ''
        self.db = ''
        self.collection = ''
    
    def connection_mongodb(self):
        self.url = 'mongodb://admin:mysterico@k8s.mysterico.com:31489'
        self.connection = MongoClient(self.connection_url)
        self.db = self.connection.get_database('data_voucher')
    
    def set_collection(self, collection_name):
        self.collection = self.db.get_collection(collection_name)
    

