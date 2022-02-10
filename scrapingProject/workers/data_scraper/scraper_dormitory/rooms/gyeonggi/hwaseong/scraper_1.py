from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 하남시

# 타겟 : 도정소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.hscity.go.kr/www/gnews/BD_selectGnewsList.do?q_totalCnt=&q_currPage={}&q_rowPerPage=10&q_caCode=&q_beCode=C001
    header :
        None

'''
'''
    @post info
    method : POST
    url : https://www.hscity.go.kr/www/gnews/BD_selectGnewsDetail.do
    header :
        None
    body :
        1. q_caCode = {post_id}
        2. q_beCode = C001

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '화성시'
        self.post_board_name = '도정소식'
        self.channel_main_url = 'https://www.hscity.go.kr'
        self.post_url = 'https://www.hscity.go.kr/www/gnews/BD_selectGnewsDetail.do'

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
        'multiple_type': ['contents_req_params', 'post_title', 'uploader', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-7 HYUN
    # html table header index
    table_column_list = ['순번', '제목', '등록자', '등록일자']

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

            if idx == 1:
                var['post_title'].append(tmp_td.text.strip())
                # javascript:jsDetail('202202030937265164C048', 'C001');
                # ['contents_req_params']
                post_move_function_str = tmp_td.find('a').get('href').strip()
                post_move_param_list = eval('[' + str_grab(post_move_function_str, 'jsDetail(', ');') + ']')

                post_move_params = {
                    'q_caCode': post_move_param_list[0],
                    'q_beCode': post_move_param_list[1]
                }

                var['contents_req_params'].append(post_move_params)
            elif idx == 2:
                var['uploader'].append(tmp_td.text.strip())
            elif idx == 3:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip().replace('.0', '')))

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
    context_area = soup.find('div', class_='gallery_view_con')

    var['post_text'] = clean_text(context_area.text).strip()
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result