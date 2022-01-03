from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 방위사업청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : POST
    url =  http://www.dapa.go.kr/dapa/na/ntt/selectNttList.do
    header :
        1.Content-Type: application/x-www-form-urlencoded
    body :
        1. currPage = {page_count}
        2. bbsId = 443
    required data searching point :
        header_1 : fixed
        body_1 = page_count
        body_2 = fixed
'''
'''
    @post info
    method : GET
    url : http://www.dapa.go.kr/dapa/na/ntt/selectNttInfo.do?bbsId=443&nttSn={postId}&menuId=356
    header :
        None

'''
sleep_sec = 1
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '방위사업청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'http://www.dapa.go.kr'
        self.post_url = 'http://www.dapa.go.kr/dapa/na/ntt/selectNttInfo.do?bbsId=443&nttSn={}&menuId=356'
        
    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded"))
        self.session = set_headers(self.session, self.additional_key_value, isUpdate)
        self.page_count = 1
        while True :
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
        data = {
            "currPage" : self.page_count,
            "bbsId" : 443
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)