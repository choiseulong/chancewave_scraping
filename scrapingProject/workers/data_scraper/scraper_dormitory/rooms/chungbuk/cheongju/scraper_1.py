from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from unicodedata import normalize

# 채널 이름 : 청주시

# 타겟 : 공지사항
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.cheongju.go.kr/www/selectBbsNttList.do?key=280&bbsNo=510&searchCtgry=&pageUnit=10&searchCnd=all&searchKrwd=&integrDeptCode=000100101&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.cheongju.go.kr/www/selectBbsNttView.do?key=280&bbsNo=510&nttNo={post_id}&searchCtgry=&searchCnd=all&searchKrwd=&pageIndex=2&integrDeptCode=000100101
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '청주시'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.cheongju.go.kr/'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True:
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
        'multiple_type': ['post_url', 'post_title', 'uploaded_time', 'view_count']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-8 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '부서', '파일', '조회수', '작성일']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='bbs_default_list')

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
            if tmp_td.text.find('등록된 게시물이 없습니다.') > -1:
                print('PAGE END')
                return
            if idx == 1:
                var['post_title'].append(tmp_td.text.strip())
                var['post_url'].append(
                    make_absolute_url(in_url=tmp_td.find('a').get('href'),
                                      channel_main_url=var['response'].url))
            elif idx == 4:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text))
            elif idx == 5:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):

    target_key_info = {
        'single_type': ['post_text', 'uploader', 'contact'],
        'multiple_type': ['post_image_url']
    }

    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='bbs_basic')

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '제목':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '연락처':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '담당자':
                if var.get('uploader') and var.get('uploader') != tmp_info_value_text:
                    var['uploader'] = var['uploader'] + ' ' + tmp_info_value_text
                else:
                    var['uploader'] = tmp_info_value_text

            elif tmp_info_title_text == '부서':
                if var.get('uploader') and var.get('uploader') != tmp_info_value_text:
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '내용':
                var['post_text'] = tmp_info_value_text
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result