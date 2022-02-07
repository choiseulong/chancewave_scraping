from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 포천시

# 타겟 : 문화/공연
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.pocheon.go.kr/www/selectBbsNttList.do?bbsNo=25&key=3101&pageUnit=10&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.pocheon.go.kr/www/selectBbsNttView.do?bbsNo=25&nttNo={post_id}&key=3101&pageUnit=10&pageIndex=1
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '포천시'
        self.post_board_name = '문화/공연'
        self.channel_main_url = 'https://www.pocheon.go.kr/'

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
        'multiple_type': ['post_url', 'post_title', 'view_count', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '파일', '조회수', '작성일', '수정일']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', id='board')

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

            if idx == 0:
                if tmp_td.text.strip() == '[공지]':
                    break
                # 게시물이 없는 경우 & 페이지 끝
                elif tmp_td.text.strip().find('등록된 게시물이 없습니다') > -1:
                    print('PAGE END')
                    return
            elif idx == 1:
                var['post_title'].append(tmp_td.text.strip())
                var['post_url'].append(make_absolute_url(in_url=tmp_td.find('a').get('href').strip(), channel_main_url=var['response'].url))
            elif idx == 3:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))
            elif idx == 4:
                if tmp_td.text.strip():
                    var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
                else:
                    var['uploaded_time'].append(None)

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
    content_info_area = soup.find('table', class_='bbs_default').find('td', class_='bbs_content')

    var['post_text'] = clean_text(content_info_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(content_info_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result