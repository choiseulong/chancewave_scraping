from workers.dataServer.mongoServer import MongoServer
from workers.dataScraper.scrapingManager import ScrapingManager 

class ProjectManager:
    def __init__(self):
        self.TargetDateRange = None
        self.scrapingManager = ScrapingManager()
    
    def job_init_with_target_date(self, targetDate:dict):
        self.TargetDateRange = self.scrapingManager.get_date_range(targetDate)
        self.scrapingManager.scraping_worker_job_init()
    
    def get_data(self, channelCode=''):
        mongo = MongoServer()
        if channelCode:
            data = mongo.get_data(channelCode)
        else :
            data = mongo.get_total_data()
        return data






    
        

