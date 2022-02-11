from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 용인시

# 타겟 : 교육안내
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : http://www.yongin.go.kr/edu/institutionNLecture/lctrs/BD_selectCteduLctrsList.do?q_lftmEdcRealm=&q_lftmEdcTrget=&q_searchYear=&q_searchMonth=&q_searchKey=&q_searchVal=&q_currPage={page_count}&q_sortName=&q_sortOrder=&

    header :
        None

'''

sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '용인시'
        self.post_board_name = '교육안내'
        self.channel_main_url = 'https://www.yongin.go.kr'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)
        self.session = set_headers(self.session)
        self.page_count = 1
        while True:
            print(f'PAGE {self.page_count}')

            self.channel_url = self.channel_url_frame.format(self.page_count)

            self.post_list_scraping(post_list_parsing_process, 'get')
            if self.scraping_target:
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
            else:
                break

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_title', 'post_subject', 'start_date', 'end_date',  'start_date2',
                          'end_date2', 'extra_info', 'linked_post_url']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '분류', '강좌명', '운영기관', '홈페이지', '기간']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='t_list')

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
            tmp_value_text = clean_text(tmp_td.text).strip()
            if idx == 0:
                if tmp_td.text.find('데이터가 존재하지 않습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                var['post_subject'].append(tmp_value_text)
            elif idx == 2:
                tmp_move_link = make_absolute_url(
                        in_url=tmp_td.find('a').get('href'),
                        channel_main_url=var['response'].url
                    )
                var['post_title'].append(tmp_value_text)
                var['post_url'].append(tmp_move_link)
                var['linked_post_url'].append(tmp_move_link)
            elif idx == 3:
                var['extra_info'].append([
                    {
                        'info_title': '교육상세',
                        'info_1': ['운영기관', tmp_value_text]
                    }])
            elif idx == 5:
                [f.decompose() for f in tmp_td.find_all('span')]
                tmp_period_str_list = [f.strip() for f in tmp_td.children if not f.name]
                tmp_period_str_list = [f for f in tmp_period_str_list if f]
                apply_period_str_all = tmp_period_str_list[0]
                apply_period_str_list = [f.strip() for f in apply_period_str_all.split('~')]

                program_period_str_all = tmp_period_str_list[1]
                program_period_str_list = [f.strip() for f in program_period_str_all.split('~')]

                var['start_date'].append(convert_datetime_string_to_isoformat_datetime(apply_period_str_list[0]))
                var['end_date'].append(convert_datetime_string_to_isoformat_datetime(apply_period_str_list[1]))

                var['start_date2'].append(convert_datetime_string_to_isoformat_datetime(program_period_str_list[0]))
                var['end_date2'].append(convert_datetime_string_to_isoformat_datetime(program_period_str_list[1]))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result
