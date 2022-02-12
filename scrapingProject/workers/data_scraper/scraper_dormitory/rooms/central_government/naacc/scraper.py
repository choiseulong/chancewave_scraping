from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from .parser import *

# 채널 이름 : 행정중심복합도시건설청

# 타겟 : 모든 공고
# 중단 시점 : 마지막 페이지 도달시

#HTTP Request
'''
    @post list

    method : GET
    url =  https://www.naacc.go.kr/csi_board/csi_boardList.do?menu_id=notice&currentPage={}
    header :
        Cookie : JSESSIONID=CzmAdk8thWocQB7+1BnaZayp.node10
    required data searching point :
        header_1 : 메인페이지에서 쿠키 받아옴
'''
'''
    @post info
    method : GET
    url : https://www.naacc.go.kr/csi_board/csi_boardView.do?menu_id=notice&num={postId}
    header :
        Cookie : JSESSIONID=CzmAdk8thWocQB7+1BnaZayp.node10
    required data searching point :
        header_1 : 메인페이지에서 쿠키 받아옴
'''
sleep_sec = 1
is_update = True

class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '행정중심복합도시건설청'
        self.post_board_name = '알립니다'
        self.post_url = 'https://www.naacc.go.kr/WEB/contents/N3010000000.do?schM=view&id={}'
        
    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
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
        # if self.page_count == 1 :
        #     status, response = get_method_response(self.session, self.channel_main_url)
        #     if status == 'ok' :
        #         JSESSIONID = response.cookies.get_dict()['JSESSIONID']
        #         self.additional_key_value.append(("Cookie", f"JSESSIONID={JSESSIONID}"))
        #         self.session = set_headers(self.session, self.additional_key_value, is_update)
        super().post_list_scraping(post_list_parsing_process, 'get', sleep_sec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleep_sec)