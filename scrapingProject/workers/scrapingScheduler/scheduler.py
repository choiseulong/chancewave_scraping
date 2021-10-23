from datetime import datetime
from pytz import timezone
from workers.dataServer.mongoServer import MongoServer

class Scheduler:
    def __init__(self):
        self.scrapingHistory = 'scrapingHistory'
        self.now = ''

    def check(self):
        self.now = datetime.now(timezone('Asia/Seoul'))
        pass

    def connection_mongo(self, collectionName):
        MongoServer().connection_mongodb().set_collection(collectionName)

    def insert_new_target_channel(self, channelUrl):
        self.connection_mongo(self.scrapingHistory)