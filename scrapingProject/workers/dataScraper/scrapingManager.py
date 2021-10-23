from workers.dataScraper.scraperTools.tools import *
from ..dataServer.mongoServer import MongoServer
import requests as req
import importlib

class ScrapingManager:
    def __init__(self):
        self.channelUrlList = []
    
    def get_requests_session(
            self, 
            proxies = {
                "http": "http://127.0.0.1:8889", 
                "https":"http:127.0.0.1:8889"
            }
        ):
        session = req.Session()
        session.verify = r'./workers/dataScraper/scraperTools/FiddlerRoot.pem'
        session.proxies = proxies
        return session
    
    def get_channel_url(self):
        mongoServer = MongoServer()
        channelData = mongoServer.serve_channel_data()
        for i in channelData:
            channelUrl = i['channelUrl']
            self.channelUrlList.extend(channelUrl)

    def get_scraped_response(self):
        self.get_channel_url()
        for UrlData in self.channelUrlList:
            session = self.get_requests_session()
            channelCode, channelUrl = return_key_value(UrlData)
            tmp = importlib.import_module(f'workers.dataScraper.scraper.{channelCode}')
            tmp.scraping_response(session, channelCode, channelUrl)
            # result = scraper.scraping_response(session, channelCode, channelUrl)
            break