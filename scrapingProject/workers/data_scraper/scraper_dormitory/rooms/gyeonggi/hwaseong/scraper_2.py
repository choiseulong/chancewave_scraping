from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 하남시

# 타겟 : 타기관 공고/고시
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.hscity.go.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1088&q_bbscttSn=&q_seachType=where&q_deptCodeSelect=1001&q_searchWhereTy=AND&q_searchVal=&q_searchStartDt=&q_searchEndDt=&q_currPage={page_count}&q_sortName=&q_sortOrder=&
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.hscity.go.kr/www/user/bbs/BD_selectBbs.do?q_bbsCode=1088&q_bbscttSn={post_id}
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '화성시'
        self.post_board_name = '타기관 공고/고시'
        self.channel_main_url = 'https://www.hscity.go.kr'

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
        'multiple_type': ['post_url', 'uploader', 'post_title']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-7 HYUN
    # html table header index
    table_column_list = ['순번', '', '제목', '담당부서', '등록일자']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='board_list')

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
            if tmp_td.text.find('데이터가 존재하지 않습니다') > -1:
                print('PAGE END')
                return

            if idx == 2:
                var['post_title'].append(tmp_td.text.strip())
                var['post_url'].append(make_absolute_url(in_url=tmp_td.find('a').get('href').strip(), channel_main_url=var['response'].url))
            elif idx == 3:
                var['uploader'].append(tmp_td.text.strip())

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
    content_info_area = soup.find('div', class_='sub_rgtCon').find('tbody')

    content_info_row_list = content_info_area.find_all('tr')

    for tmp_info_row in content_info_row_list:
        tmp_column_title_area_list = tmp_info_row.find_all('th')
        tmp_column_value_area_list = tmp_info_row.find_all('td')
        for tmp_column_title_area, tmp_column_value_area in zip(tmp_column_title_area_list, tmp_column_value_area_list):
            tmp_column_title_text = tmp_column_title_area.text.strip()
            tmp_column_value_text = clean_text(tmp_column_value_area.text).strip()

            if tmp_column_title_text == '내용':
                var['post_text'] = clean_text(tmp_column_value_text)
                var['post_image_url'] = search_img_list_in_contents(tmp_column_value_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result