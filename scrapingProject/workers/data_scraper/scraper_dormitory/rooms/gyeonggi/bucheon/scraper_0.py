from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 부천

# 타겟 : 시정소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.bucheon.go.kr/site/program/board/basicboard/list?boardtypeid=26736&menuid=148002001001&pagesize=10&currentpage={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.anyang.go.kr/main/selectBbsNttView.do?key=259&bbsNo=62&nttNo={postId}&searchCtgry=&searchKrwd=&pageIndex=1&integrDeptCode=
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '부천'
        self.post_board_name = '새소식'
        self.channel_main_url = 'https://www.bucheon.go.kr'

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

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'view_count', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-18 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '담당부서', '담당자', '작성일', '조회수']

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

            elif idx == 1:
                page_move_function_str = tmp_td.find('a').get('href').strip()
                var['post_url'].append(make_absolute_url(
                    in_url=page_move_function_str,
                    channel_main_url=var['response'].url))
            elif idx == 4:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 5:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

    result = merge_var_to_dict(key_list, var)
<<<<<<< HEAD
=======
    if var['dev']:
        print(result)
>>>>>>> dev_hyun
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'contact', 'uploader'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='table-style')
    var['post_title'] = content_info_area.find('th', class_='title').text.strip()
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '전화번호':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '작성자':
                if var.get('uploader'):
                    var['uploader'] = var['uploader'] + ' ' + tmp_info_value_text
                else:
                    var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '부서':
                if var.get('uploader'):
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_info_value_text

    context_area = content_info_area.find('div', class_='board-cons')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
<<<<<<< HEAD
=======
    if var['dev']:
        print(result)
>>>>>>> dev_hyun
    return result