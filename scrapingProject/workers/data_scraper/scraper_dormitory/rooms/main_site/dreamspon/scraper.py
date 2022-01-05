from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 드림스폰

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시


#HTTP Request
'''
    @post list

    method : GET
    url = https://www.dreamspon.com/scholarship/list.html?page={page_count}
    header :
        None
'''
'''
    @post info
    method : GET
    url : post_url
    header :
        None
'''

sleep_sec = 1
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '드림스폰'
        self.post_board_name = '일반장학금'
        self.channel_main_url = 'https://www.dreamspon.com'
    
    def scraping_process(self, channel_code, channel_url):
        super().scraping_process(channel_code, channel_url)
        self.page_count = 1
        status = self.login_process()
        if status :
            while True :
                self.session = set_headers(self.session)
                self.channel_url = self.channel_url_frame.format(self.page_count)
                self.post_list_scraping()
                if self.scraping_target :
                    self.target_contents_scraping()
                    self.collect_data()
                    self.mongo.reflect_scraped_data(self.collected_data_list)
                    self.page_count += 1
                else :
                    break
 
    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)
    
    def login_process(self):
        url = 'https://www.dreamspon.com/process/checkuser.html'
        data = {
            "mode" : "login",
            "userid" : "chancewave@mysterico.com",
            "pageReferer" : 'https://www.dreamspon.com/',
            "userpw" : "mysterico"
        }
        self.additional_key_value.append(['Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'])
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)
        _, response = post_method_response(self.session, url, data)
        if response.json()['checkyn'] == 'Y' :
            return True
        else :
            return False
       



            

 



