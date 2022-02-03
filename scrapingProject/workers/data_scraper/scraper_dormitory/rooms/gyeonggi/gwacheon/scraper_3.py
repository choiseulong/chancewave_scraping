import js2py

from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 과천시

# 타겟 : 보건소 새소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url :  https://www.gccity.go.kr/ghc/bbs/list.do?ptIdx=111&mId=0801000000&page={page_count}
    header :
        None
    body :
        None

'''
'''
    @post info
    method : GET
    url :  https://www.gccity.go.kr/ghc/bbs/view.do?mId=0801000000&bIdx={post_id}&ptIdx=111
    header :
        None
    body :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '과천시'
        self.post_board_name = '보건소 새소식'
        self.channel_main_url = 'https://www.gccity.go.kr'

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
        'multiple_type': ['post_url', 'post_subject', 'post_title',  'uploaded_time', 'view_count']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    site_js_object_text = str_grab(text, 'var yh = {', '};')
    site_js_object = js2py.eval_js('var yh = {' + site_js_object_text + '}')

    # 2022-2-3 HYUN
    # html table header index
    table_column_list = ['번호', '분류', '제목', '파일', '작성자', '작성일', '조회']

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

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            # 게시물이 없는 경우 & 페이지 끝
            tmp_td_text = tmp_td.text.strip()

            if idx == 0:
                if tmp_td.find('img', {'alt':'공지'}) and var['page_count'] != 1:
                    break
            elif idx == 1:
                var['post_subject'].append(clean_text(tmp_td_text))
            elif idx == 2:
                # '새 글' 이 제목에 함께 포함되는 부분 제거
                var['post_title'].append(tmp_td_text.split('\n')[0])
                # goTo.view('list','157354','111','0301010000')
                move_page_js_function_text = tmp_td.find('a').get('onclick')
                move_page_js_function_params_text = str_grab(move_page_js_function_text, 'view(', ');')
                move_page_js_function_params_list = eval('[' + move_page_js_function_params_text + ']')
                tmp_post_url = site_js_object['contextPath'] + "/" + site_js_object['siteCodeFull'] + \
                               "/bbs/view.do?mId=" + site_js_object['mId'] + \
                               "&bIdx=" + move_page_js_function_params_list[1] + \
                               "&ptIdx=" + move_page_js_function_params_list[2]

                var['post_url'].append(make_absolute_url(in_url=tmp_post_url, channel_main_url=var['response'].url))
            elif idx == 5:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td_text))
            elif idx == 6:
                var['view_count'].append(tmp_td_text)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'uploader'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    content_info_area = soup.find('div', class_='view_info')

    # 작성자 영역
    uploader_area = content_info_area.find('li', class_='view_write')
    if uploader_area.span.text.strip() != '작성자':
        raise ValueError('Please check uploader area')
    var['uploader'] = clean_text(uploader_area.span.nextSibling.text).split(':')[1].strip()

    context_area = soup.find('div', class_='view_cont')

    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result
