from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 국세청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list
    method : POST
    url = https://www.nts.go.kr/nts/na/ntt/selectNttList.do
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.moef.go.kr/nw/nes/detailNesDtaView.do?searchBbsId1={MOSFBBS}&searchNttId1={MOSF}
    header :
        None
'''

sleep_sec = 3
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '국세청'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.nts.go.kr'
        self.post_url = 'https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do'
        
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
            "bbsId" : 1011
        }
        super().post_list_scraping(post_list_parsing_process, 'post', data, sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)


            

 



