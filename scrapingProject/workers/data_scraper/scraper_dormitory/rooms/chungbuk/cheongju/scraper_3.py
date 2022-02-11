from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from unicodedata import normalize

# 채널 이름 : 청주시

# 타겟 : 의료원소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.cjmc.or.kr/bbs/board.php?bo_table=notice&page={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.cjmc.or.kr:443/bbs/board.php?bo_table=notice&wr_id={post_id}&page=1
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '청주시'
        self.post_board_name = '의료원소식'
        self.channel_main_url = 'https://www.cjmc.or.kr/'

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
        'multiple_type': ['post_url', 'post_title', 'uploader', 'view_count']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-8 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '글쓴이', '날짜', '조회']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='tbl_wrap').find('table')

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
                var['post_url'].append(tmp_td.find('a').get('href'))
            elif idx == 2:
                var['uploader'].append(tmp_td.text.strip())
            elif idx == 4:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text))


    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):

    target_key_info = {
        'single_type': ['post_text', 'uploaded_time'],
        'multiple_type': ['post_image_url']
    }

    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    header_info_area = soup.find('section', id='bo_v_info')
    uploaded_time_area = header_info_area.find('span', string='작성일').nextSibling
    var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime('20' + uploaded_time_area.text)

    context_area = soup.find('div', id='bo_v_con')

    var['post_text'] = clean_text(context_area.text).strip()
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result