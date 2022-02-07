from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 의정부시
# 타겟 : 공고
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.ui4u.go.kr/portal/recruit/anm/list.do?mId=0406010100&page={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.ui4u.go.kr/portal/recruit/anm/view.do?mId=0406010100&idx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '의정부시'
        self.post_board_name = '공고'
        self.channel_main_url = 'https://www.ui4u.go.kr/'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        # self.channel_url = 'https://www.pyeongtaek.go.kr/pyeongtaek/bbs/list.do?ptIdx=41&mId=0401010000&bIdx='
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
        'multiple_type': ['post_url', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '공고 제목', '접수 기간', '모집 인원(우선/일반)', '지원 현황', '접수 상태']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='bod_list')

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

            if idx == 1:
                post_idx = tmp_td.find('a').get('onclick').strip()
                post_idx = str_grab(post_idx, "go_view('", "');")

                var['post_url'].append(make_absolute_url(
                    in_url='/portal/recruit/anm/view.do?mId=0406010100&idx=' + post_idx,
                    channel_main_url=var['response'].url
                ))
            elif idx == 5:
                if tmp_td.text.find('접수마감') > -1:
                    var['is_going_on'].append(False)
                else:
                    var['is_going_on'].append(True)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'start_date', 'uploader', 'end_date', 'end_date2', 'contact'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='tbl_form')
    var['extra_info'] = [{
        'info_title': '공고 상세'
    }]
    extra_info_column_list = ['추첨 방식']

    for tmp_row_area in content_info_area.find_all('dl'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('dt'), tmp_row_area.find_all('dd')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '공고 제목':
                var['post_title'] = tmp_info_value_text
            if tmp_info_title_text == '접수 기간':
                tmp_date_period_str = tmp_info_value_text
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:

                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
            elif tmp_info_title_text == '합격자 발표일':
                var['end_date2'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
            elif tmp_info_title_text == '문의처':
                if tmp_info_value_text.find('(') > -1:
                    var['contact'] = str_grab(tmp_info_value_text, '(', '')[:-1]
                    var['uploader'] = str_grab(tmp_info_value_text, '', '(')
                else:
                    var['contact'] = tmp_info_value_text
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '내용':
                var['post_text'] = clean_text(tmp_info_value.text.strip())
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result