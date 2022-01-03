from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# youthcenter_0 : 청년정책 통합검색
# 타겟 : 모든 포스트

# HTTP Request
'''
    @post list 

    method : get
    url : https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1
    header : none
'''
'''
    @post info

    method : post
    url : https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do
    header : 
        1. Content-Type: application/x-www-form-urlencoded 
        2. Cookie: YOUTHCENTERSESSIONID=CjoODAtum_PuuKthsJaMypZLqg4b5HlmNsEt8eKzphA686yPkRR_!1041055556!1126342983;
    body :
        _csrf=072abdbd-ecab-4fcb-bb99-5acec3572242&bizId=R2021021800010
        1. _csrf=04baa83b-492c-415c-9820-94ab677331a9
        2. bizId=R2021021800010
    required data searching point :
        header_1 : fixed
        header_2 : dynamic 
            get <@post list> header Cookie and parsing
        body_1 : dynamic 
            find <@post list> html tag attrs['content']
                <meta name="_csrf" content="04baa83b-492c-415c-9820-94ab677331a9" />
        body_2 : dynamic 
            find <@post list> html tag attrs['value'] and parsing
                <span class="checkbox">
						<input type="checkbox" class="checkbox" id="cmprCheckboxR2021021800010" name="cmprCheckbox" value="R2021021800010">
						<label for="cmprCheckboxR2021021800010"><span class="blind"><em>국민취업지원제도</em>선택</span></label>
                </span>	
'''
isUpdate = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '온라인청년센터'
        self.post_board_name = '청년정책 통합검색'
        self.post_url = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do'

    def scraping_process(self, channel_code, channel_url, date_range):
        super().scraping_process(channel_code, channel_url, date_range)
        # self.mongo.remove_channel_data(channel_code)
        self.page_count = 1
        while True :
            self.session = set_headers(self.session)
            self.channel_url = self.channel_url_frame.format(self.page_count)
            self.post_list_scraping()

            if not self.scraping_target:
                break
            
            if isinstance(self.scraping_target, list):
                self.additional_key_value.extend(find_request_params(self.scraping_target, ['Cookie'])) 
                for i in range(len(self.additional_key_value)):
                    del self.scraping_target[-(i+1)]
                self.additional_key_value.append(("Content-Type", "application/x-www-form-urlencoded "))
                self.session = set_headers(self.session, self.additional_key_value, isUpdate)
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
                self.empty_page_count = 0

                #쿠키 초기화
                self.session.cookies.clear()
                self.additional_key_value = []
            elif self.scraping_target == 'endpoint' : break
                
    
    def post_list_scraping(self):
        super().post_list_scraping(post_list_parsing_process, 'get')
    
    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process)
    



