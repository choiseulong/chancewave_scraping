from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 의정부시
# 타겟 : 행사목록
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.ui4u.go.kr/portal/eventNoti/list.do?mId=0301170100&page={page_count}
    header :
        None

'''

sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '의정부시'
        self.post_board_name = '행사목록'
        self.channel_main_url = 'https://www.ui4u.go.kr/'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        # self.channel_url = 'https://www.pyeongtaek.go.kr/pyeongtaek/bbs/list.do?ptIdx=41&mId=0401010000&bIdx='
        self.session = set_headers(self.session)
        self.page_count = 1
        while True:
            print(f'PAGE {self.page_count}')

            self.channel_url = self.channel_url_frame.format(self.page_count)

            self.post_list_scraping(post_list_parsing_process, 'get')
            if self.scraping_target:
                # self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else:
                break


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_title', 'uploader', 'start_date', 'end_date', 'extra_info', 'post_url_can_use']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '시작일', '종료일', '장소', '담당부서']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='bod_list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('thead')
    # 테이블 칼럼 리스트
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')

    # 테이블 컬럼명 검증 로직
    for column_idx, tmp_header_column in enumerate(post_list_table_header_list_bs):
        if table_column_list[column_idx] != tmp_header_column.text.strip():
            print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {tmp_header_column.text.strip()}')
            raise('List Column Index Change')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:
        var['post_url_can_use'].append(False)
        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            tmp_info_value_text = clean_text(tmp_td.text).strip()
            if idx == 1:
                var['post_title'].append(tmp_info_value_text)
            elif idx == 2:
                var['start_date'].append(convert_datetime_string_to_isoformat_datetime(tmp_info_value_text))
            elif idx == 3:
                var['end_date'].append(convert_datetime_string_to_isoformat_datetime(tmp_info_value_text))
            elif idx == 4:
                var['extra_info'].append(
                    [{
                        'info_title': '행사 상세',
                        'info_1': ['장소', tmp_info_value_text]
                    }]
                )
            elif idx == 5:
                var['uploader'].append(tmp_info_value_text)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result
