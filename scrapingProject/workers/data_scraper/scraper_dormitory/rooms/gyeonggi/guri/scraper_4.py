from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 구리

# 타겟 : 보건소 공지사항
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.guri.go.kr/brd/board/1026/L/CATEGORY/2526/menu/3286?brdType=L&searchField=&searchText=&thisPage={page_cout}&type=
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.guri.go.kr/brd/board/1026/L/CATEGORY/2526/menu/3286?brdType=R&thisPage=1&bbIdx={post_id}=&searchField=&searchText=
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '구리'
        self.post_board_name = '보건소 공지사항'
        self.channel_main_url = 'https://www.guri.go.kr'

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

    # def post_list_scraping(self):
    ## post 방식이라면 super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)
    #     super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-3 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '첨부', '담당부서', '작성일', '조회']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='board_wrap_bbs').find('table')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('thead')
    # 테이블 칼럼 리스트
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            # 게시물이 없는 경우 & 페이지 끝
            if tmp_td.text.find('현재 게시글이 없습니다.') > -1:
                print('PAGE END')
                return

            if idx == 0:
                if tmp_td.text.strip() == '공지':
                    # 번호에 공지가 있는 경우 리스트에 중복 출현하므로 처리 X
                    break
            elif idx == 1:
                var['post_url'].append(var['channel_main_url'] + tmp_td.find('a').get('href'))
            elif idx == 4:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 5:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'uploader'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='board_wrap_bbs').find('table')

    content_info_header_area = content_info_area.find('thead')
    content_info_header_row_list = content_info_header_area.find_all('tr')

    for tmp_header_row in content_info_header_row_list:
        tmp_column_title_area_list = tmp_header_row.find_all('th')
        tmp_column_value_area_list = tmp_header_row.find_all('td')
        for tmp_column_title_area, tmp_column_value_area in zip(tmp_column_title_area_list, tmp_column_value_area_list):
            tmp_column_title_text = tmp_column_title_area.text.strip()
            tmp_column_value_text = tmp_column_value_area.text.strip()

            if tmp_column_title_text == '제목':
                var['post_title'] = clean_text(tmp_column_value_text)
            elif tmp_column_title_text == '담당자':
                if var.get('uploader'):
                    var['uploader'] = var['uploader'] + ' ' + tmp_column_value_text
                else:
                    var['uploader'] = tmp_column_value_text
            elif tmp_column_title_text == '담당부서':
                if var.get('uploader'):
                    var['uploader'] = tmp_column_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_column_value_text

    content_context_area = content_info_area.find('tbody')
    content_context_area = content_context_area.find('td', class_='context')
    var['post_text'] = clean_text(content_context_area.text)
    var['post_image_url'] = search_img_list_in_contents(content_context_area, var['channel_main_url'])

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result