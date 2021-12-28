from workers.data_server.mongo_server import mongo_server
from workers.data_scraper.scraping_manager import scraping_manager 

class project_manager:
    def __init__(self):
        self.TargetDateRange = None
        self.scraping_manager = scraping_manager()
    
    def job_init_with_target_date(self, targetDate:dict):
        self.TargetDateRange = self.scraping_manager.get_date_range(targetDate)
        self.scraping_manager.scraping_worker_job_init()
    
    def get_data(self, channel_code=''):
        mongo = mongo_server()
        if channel_code:
            data = mongo.get_data(channel_code)
        else :
            data = mongo.get_total_data()
        return data






    
        

