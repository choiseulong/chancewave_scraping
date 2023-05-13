from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 서대문구

# 타겟 : 복지 장애인복지사업
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.sdm.go.kr/news/news/notice.do?cp={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.sdm.go.kr/welfare/handicapped/business.do?cp=1&sdmBoardSeq={postId}&mode=view
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '서대문구'
        self.post_board_name = '복지 장애인복지사업'
        self.channel_main_url = 'https://www.sdm.go.kr'

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
            self.session.cookies.clear()

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'view_count', 'post_title', 'uploader', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-27 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '작성자', '등록일', '조회수']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='boardList')

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

            if idx == 1:
                post_id_str = str_grab(tmp_td.find('a').get('href'), "goView('", "')")
                tmp_query_param = {
                    'sdmBoardSeq': post_id_str,
                    'mode':'view'
                }
                query = urlencode(tmp_query_param)
                var['post_url'].append(var['response'].url + '&' + query)
                var['post_title'].append(clean_text(tmp_td.find('a').text).strip())
            elif idx == 2:
                var['uploader'].append(clean_text(tmp_td.text).strip())
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
        'single_type': ['post_text'],
        'multiple_type': ['post_image_url']
    }

    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', id='sub_content')

    if content_info_area.find('table', class_='boardWrite'):
        content_info_area.find('table', class_='boardWrite').decompose()

    if content_info_area.find('div', class_='Table_board_btn_right'):
        content_info_area.find('div', class_='Table_board_btn_right').decompose()

    if content_info_area.find('div', class_='tag'):
        content_info_area.find('div', class_='tag').decompose()

    var['post_text'] = clean_text(content_info_area.text).strip()
    var['post_image_url'] = search_img_list_in_contents(content_info_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result