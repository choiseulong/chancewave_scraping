from workers.dataServer.mongoServer import MongoServer
from workers.dataParser.parser import Parser
from workers.scrapingScheduler.scheduler import Scheduler 
from workers.dataScraper.scrapingManager import ScrapingManager 

class ProjectManager:
    def __init__(self):
        self.schedule = {}
        
    def check_scraping_schedule(self):
        scheduler = Scheduler()
        self.schedule = scheduler.check()

    def channel_response_request(self):
        req_response = ScrapingManager()

    def job_init(self):
        # self.check_scraping_schedule()

        scrapingManager = ScrapingManager()
        scrapingManager.all_channels_init()
    
    def new_target_init(self, Target):
        mongoServer = MongoServer()
        result = mongoServer.insert_new_target_channel(Target)
        return result
        

