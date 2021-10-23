from datetime import datetime
from pytz import timezone
from .tools import *

class Scheduler:
    def __init__(self):
        self.scrapingHistory = 'scrapingHistory'
        self.now = ''

    def check(self):
        self.now = datetime.now(timezone('Asia/Seoul'))
        pass
