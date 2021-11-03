from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
from workers.dataScraper.parser.seoul_welfare_portal import *
from workers.dataServer.mongoServer import MongoServer
from .seoul_welfare_portal_0 import Scraper as default_scraper

class Scraper(default_scraper):
    pass