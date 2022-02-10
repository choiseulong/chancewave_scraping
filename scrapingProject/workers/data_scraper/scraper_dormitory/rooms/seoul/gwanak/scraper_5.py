from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py
from urllib.parse import urlencode


# 채널 이름 : 관악구

# 타겟 : 보건소 새소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.gwanak.go.kr/site/health/ex/bbs/List.do?cbIdx=275&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gwanak.go.kr/site/health/ex/bbs/View.do?cbIdx=275&bcIdx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '관악구'
        self.post_board_name = '보건소 새소식'
        self.channel_main_url = 'https://www.gwanak.go.kr'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
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
            self.session.cookies.clear()

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'view_count', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-31 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '담당부서', '작성일', '조회수']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', id='boardDivId')
    post_list_table_bs = post_list_table_bs.find('table', class_='list')

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

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                if tmp_td.text.find('등록된 게시글이 없습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                # doBbsFView(cbIdx, bcIdx, Gbn, parentSeq)
                # doBbsFView('239','126615','16010100','126615');return false;

                page_move_function_str = clean_text(tmp_td.find('a').get('onclick'))
                tmp_parameter_str = str_grab(page_move_function_str, 'doBbsFView(', ');')
                parameter_list = eval('[' + tmp_parameter_str + ']')

                tmp_cb_idx = parameter_list[0]
                tmp_bc_idx = parameter_list[3]

                tmp_query_param = {
                    'cbIdx': tmp_cb_idx,
                    'bcIdx': tmp_bc_idx
                }

                tmp_query = urlencode(tmp_query_param)

                var['post_url'].append(make_absolute_url(
                    in_url='/site/health/ex/bbs/View.do?' + tmp_query,
                    channel_main_url=var['response'].url))
            elif idx == 3:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 4:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)

    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'uploader', 'contact'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='board')
    content_info_area = content_info_area.find('table', class_='view')

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '제목':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '작성자':
                if not var.get('uploader'):
                    var['uploader'] = tmp_info_value_text
                else:
                    var['uploader'] = var['uploader'] + ' ' + tmp_info_value_text
            elif tmp_info_title_text == '담당부서':
                if not var.get('uploader'):
                    var['uploader'] = tmp_info_value_text
                else:
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
            elif tmp_info_title_text == '전화번호':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '내용':
                context_area = tmp_info_value
                var['post_text'] = clean_text(context_area.text.strip())
                var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)

    return result