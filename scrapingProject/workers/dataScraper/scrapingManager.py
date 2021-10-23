from workers.dataScraper.workers.scraper import Scraper 
from workers.dataScraper.scraperTools.tools import *
from configparser import ConfigParser
import requests as req

config = ConfigParser()
config.read('./workers/dataScraper/tools/url.ini')
for section in config.sections():
    for item in list(config[section].items()):
        key = item[0] 
        value = item[1] 
        globals()[f'{key}'] = value

class ScrapingManager:
    def __init__(self):
        self.session = ''
        self.channelCodeList = []
    
    def set_requests_session(
            self, 
            proxies = {
                "http": "http://127.0.0.1:8889", 
                "https":"http:127.0.0.1:8889"
            }
        ):
        session = req.Session()
        session.verify = r'./workers/dataScraper/scraperTools/FiddlerRoot.pem'
        session.proxies = proxies
        self.session = session
    
    def all_channels_url_init(self):
        channelCodeList = filtering_channel_path_in_globals(globals())
        self.channelCodeList = channelCodeList

    
    

