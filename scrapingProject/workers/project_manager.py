from workers.data_server.mongo_server import MongoServer
from workers.data_scraper.scraping_manager import ScrapingManager 

class ProjectManager:
    def __init__(self):
        self.TargetDateRange = None
        self.scraping_manager = ScrapingManager()
    
    def job_init(self, target=False):
        self.scraping_manager.get_channel_url()
        if not target :
            self.scraping_manager.scraping_init_with_celery()
        elif target :
            self.scraping_manager.scraping_target_channel_list_synchronously()

        return 'scraping start'
    
    def get_data(self, channel_code, count, page):
        mongo = MongoServer(dev=False)
        if channel_code:
            data = mongo.get_data(channel_code, count, page)
        else :
            data = mongo.get_total_data()
        return data

    def scraping_dev_test(self, channel_code):
        # mongo = MongoServer(dev=True)
        self.scraping_manager.get_channel_url()
        self.scraping_manager.scraping_dev_test(channel_code)






    
        

