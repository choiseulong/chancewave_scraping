import bs4.element

from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 구리

# 타겟 : 평생학습프로그램
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.guri.go.kr/lll/program/org/list/menu/5301?searchCnd=&searchWrd=&schDongcd=&thisPage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.guri.go.kr/lll/program/org/view/menu/5301?prgmId={post_id}&thisPage=1&searchCnd=&searchWrd=&schDongcd=&schOrgCatecd=16
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '구리'
        self.post_board_name = '평생학습프로그램'
        self.channel_main_url = 'https://www.guri.go.kr'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True:
            print(f'PAGE {self.page_count}')
            self.channel_url = self.channel_url_frame.format(self.page_count)

            self.post_list_scraping(post_list_parsing_process, 'get')
            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else:
                break

    # def post_list_scraping(self):
    ## post 방식이라면 super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)
    #     super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'is_going_on']
    }
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-3 HYUN
    # html table header index
    table_column_list = ['번호', '강좌명', '교육기간', '교육기관', '접수방법', '수강료', '정원', '현황']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='boardList')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('dl', class_='listHead')

    # 테이블 컬럼명 검증 로직
    for column_idx, tmp_header_column in enumerate([f for f in post_list_table_header_area_bs.children if f.text.strip()]):
        if table_column_list[column_idx] != tmp_header_column.text.strip():
            print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {tmp_header_column.text.strip()}')
            raise ('List Column Index Change')

    post_list_table_header_area_bs.decompose()

    post_row_list = post_list_table_bs.find_all('dl', recursive=False)

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate([f for f in tmp_post_row.children if type(f) is not bs4.element.NavigableString]):
            if idx == 1:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url
                ))
            elif idx == 7:
                if clean_text(tmp_td.text).strip() == '신청가능':
                    var['is_going_on'].append(True)
                else:
                    var['is_going_on'].append(False)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_title', 'contact', 'start_date', 'end_date', 'start_date2', 'end_date2',
                        'linked_post_url'],
        'multiple_type': ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['extra_info'] = [{
        'info_title': '프로그램 상세'
    }]
    content_info_area = soup.find('div', class_='boardWrap')

    title_area = content_info_area.find('strong', class_='programName')
    var['post_title'] = clean_text(title_area.text).strip()

    content_info_header_area = content_info_area.find('div', class_='boardView')
    content_info_header_row_list = content_info_header_area.find_all('dl')

    for tmp_header_row in content_info_header_row_list:
        tmp_column_title_area_list = tmp_header_row.find_all('dt')
        tmp_column_value_area_list = tmp_header_row.find_all('dd')
        for tmp_column_title_area, tmp_column_value_area in zip(tmp_column_title_area_list, tmp_column_value_area_list):
            tmp_info_title = tmp_column_title_area.text.strip()
            tmp_info_value = tmp_column_value_area.text.strip()

            if tmp_info_title == '접수기간':
                if tmp_info_value.find('~') > -1:
                    # 기간
                    tmp_date_period_str = tmp_info_value
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:
                        var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                    else:
                        var['start_date'] = ''
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                else:
                    # 하루
                    one_day_date_str = clean_text(tmp_info_value).strip()
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
            elif tmp_info_title == '교육기간':
                if tmp_info_value.find('~') > -1:
                    # 기간
                    tmp_date_period_str = tmp_info_value
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:
                        var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                    else:
                        var['start_date2'] = ''
                        var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                else:
                    # 하루
                    one_day_date_str = clean_text(tmp_info_value).strip()
                    var['start_date2'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
                    var['end_date2'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)

            elif tmp_info_title == '전화번호':
                var['contact'] = clean_text(tmp_info_value)

            elif tmp_info_title == '사이트':
                var['linked_post_url'] = clean_text(tmp_info_value)

            elif tmp_info_title == '교육기관명':
                var['extra_info'][0]['info_1'] = [tmp_info_title, clean_text(tmp_info_value)]
            elif tmp_info_title == '장소':
                var['extra_info'][0]['info_2'] = [tmp_info_title, clean_text(tmp_info_value)]
            elif tmp_info_title == '강사명':
                var['extra_info'][0]['info_3'] = [tmp_info_title, clean_text(tmp_info_value)]
            elif tmp_info_title == '지역':
                var['extra_info'][0]['info_4'] = [tmp_info_title, clean_text(tmp_info_value)]
            elif tmp_info_title == '정원':
                var['extra_info'][0]['info_5'] = [tmp_info_title, clean_text(tmp_info_value)]
            elif tmp_info_title == '수강료':
                var['extra_info'][0]['info_6'] = [tmp_info_title, clean_text(tmp_info_value)]
            elif tmp_info_title == '접수방법':
                var['extra_info'][0]['info_7'] = [tmp_info_title, clean_text(tmp_info_value)]

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result