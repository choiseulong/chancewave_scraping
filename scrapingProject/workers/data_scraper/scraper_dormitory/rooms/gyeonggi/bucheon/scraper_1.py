from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 부천

# 타겟 : 교육강좌
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : http://www.bucheon.go.kr/site/program/lecture/list?act=list&menuid=148006002005&nowPage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.bucheon.go.kr/site/program/lecture/view?idx={post_id}&inst_url=&menuid=148006002005
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부천'
        self.post_board_name = '교육강좌'
        self.channel_main_url = 'https://www.bucheon.go.kr'

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

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_subject', 'start_date', 'end_date', 'start_date2', 'end_date2']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-5 HYUN
    # html table header index
    table_column_list = ['번호', '분야', '대상', '프로그램명', '교육장소', '수강료', '접수기간/교육기간', '상태']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='table-style')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    if not post_list_table_bs and soup.find('div', class_='p-empty'):
        print('PAGING END')
        return

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

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                if tmp_td.text.find('해당 게시물이 없습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 2:
                var['post_subject'].append(clean_text(tmp_td.text).strip())
            elif idx == 3:
                page_move_function_str = tmp_td.find('a').get('href').strip()
                var['post_url'].append(make_absolute_url(
                    in_url=page_move_function_str,
                    channel_main_url=var['response'].url))
            elif idx == 6:

                tmp_period_str_list = [f.strip() for f in tmp_td.children if not f.name]

                apply_period_str_all = tmp_period_str_list[0]
                apply_period_str_list = apply_period_str_all.split('~')

                program_period_str_all = tmp_period_str_list[1]
                program_period_str_list = program_period_str_all.split('~')

                var['start_date'].append(convert_datetime_string_to_isoformat_datetime(apply_period_str_list[0]))
                var['end_date'].append(convert_datetime_string_to_isoformat_datetime(apply_period_str_list[1]))

                var['start_date2'].append(convert_datetime_string_to_isoformat_datetime(program_period_str_list[0]))
                var['end_date2'].append(convert_datetime_string_to_isoformat_datetime(program_period_str_list[1]))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'contact', 'post_content_target', 'linked_post_url'],
        'multiple_type': ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='table-style')

    var['extra_info'] = [{
        'info_title': '교육 상세'
    }]

    extra_info_column_list = ['강사명', '교육기관', '교육시간', '교육장소', '수강료', '접수방법', '선별방법', '강사소개']
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '프로그램명':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '교육대상':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '강좌소개':
                var['post_text'] = tmp_info_value_text
            elif tmp_info_title_text == '문의전화':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '예약접수':
                if tmp_info_value.find('img'):
                    var['linked_post_url'] = tmp_info_value.find('a').get('href')

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result