from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py
from urllib.parse import urlencode


# 채널 이름 : 마포구

# 타겟 : 공지사항
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.mapo.go.kr/site/main/board/notice/list?cp={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.mapo.go.kr/site/main/board/notice/{postId}}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '마포구'
        self.post_board_name = '공지사항'
        self.channel_main_url = 'https://www.mapo.go.kr/'

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
        'multiple_type': ['post_url', 'uploader', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-19 HYUN
    # html table header index
    table_column_list = ['순번', '제목', '담당부서', '첨부파일', '작성일']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='bbs_list')
    post_list_table_bs = post_list_table_bs.find('table')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('tr')
    # 테이블 칼럼 리스트 thead에 있는 것이 아닌, tbody의 첫번째 row가 칼럼명
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')

    # 테이블 컬럼명 검증 로직
    for column_idx, tmp_header_column in enumerate(post_list_table_header_list_bs):
        if table_column_list[column_idx] != tmp_header_column.text.strip():
            print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {tmp_header_column.text.strip()}')
            raise('List Column Index Change')

    # 테이블 칼럼 리스트 thead에 있는 것이 아닌, tbody의 첫번째 row가 칼럼명이므로 첫번째 row 생략
    post_row_list = post_list_table_bs.find('tbody').find_all('tr')[1:]

    if not post_row_list:
        print('PAGING END')
        return
    processing_count = 0
    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                # 첫페이지 이외에는 '알림' 게시물 처리 X
                if var['page_count'] != 1 and tmp_td.find('img', {'alt':'알림'}):
                    break
                processing_count += 1
            elif idx == 1:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 2:
                var['uploader'].append(tmp_td.text.strip())
            elif idx == 4:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))

    if processing_count == 0:
        print('PAGING END')
        return

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='bbs_view')
    header_area = content_info_area.find('div', class_='bbs_view_tit')
    var['post_title'] = header_area.find('h3').text.strip()

    context_area = content_info_area.find('div', class_='bbs_view_body')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result
