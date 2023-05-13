from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 평택시

# 타겟 : 주민자치센터 교육
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.pyeongtaek.go.kr/pyeongtaek/bbs/list.do?ptIdx=192&mId=0910000000&bIdx=&page={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.pyeongtaek.go.kr/pyeongtaek/bbs/view.do?mId=0910000000&bIdx={post_id}3&ptIdx=192
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '평택시'
        self.post_board_name = '주민자치센터 교육'
        self.channel_main_url = 'https://www.pyeongtaek.go.kr'

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
        'multiple_type': ['post_url', 'post_title', 'post_subject', 'uploader', 'view_count', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '분류', '제목', '담당부서', '작성자', '작성일', '파일', '조회']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='tableSt_list')

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

    if soup.find('div', class_='no_data'):
        print('PAGE END')
        return

    for tmp_post_row in post_row_list:
        tmp_department_str = ''
        tmp_uploader_str = ''

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                pass
            elif idx == 1:
                var['post_subject'].append(tmp_td.text.strip())
            elif idx == 2:
                var['post_title'].append(tmp_td.text.strip())
                page_move_function_str = tmp_td.find('a').get('onclick').strip()
                page_move_function_params_str = str_grab(page_move_function_str, 'boardView(', '; return')
                tmp_form_id = str_grab(page_move_function_params_str, "'", "',", index=1)
                tmp_write_id = str_grab(page_move_function_params_str, "'", "',", index=3)
                tmp_type = str_grab(page_move_function_params_str, "'", "',", index=5)
                tmp_b_idx = str_grab(page_move_function_params_str, "'", "',", index=7)
                tmp_pt_idx = str_grab(page_move_function_params_str, "'", "',", index=9)
                tmp_m_id = str_grab(page_move_function_params_str, "'", "',", index=11)

                query_param = {
                    'mId': tmp_m_id,
                    'bIdx': tmp_b_idx,
                    'ptIdx': tmp_pt_idx
                }
                tmp_query_param_str = urlencode(query_param)

                var['post_url'].append(make_absolute_url(
                    in_url='/pyeongtaek/bbs/view.do', channel_main_url=var['response'].url
                ) + '?' + tmp_query_param_str)
            elif idx == 3:
                tmp_department_str = tmp_td.text.strip()
            elif idx == 4:
                tmp_uploader_str = tmp_td.text.strip()
            elif idx == 5:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 7:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

        var['uploader'].append(
            (tmp_department_str + ' ' + tmp_uploader_str).strip()
        )

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='view_cont')

    var['post_text'] = clean_text(content_info_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(content_info_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result