from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 괴산군청

# 타겟 : 교육신청
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.goesan.go.kr/www/selectEdcList.do?key=1524&searchKrwd=&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.goesan.go.kr/www/selectEdc.do?key=1524&edcNo={post_id}&searchKrwd=&pageIndex=1
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '괴산군청'
        self.post_board_name = '교육신청'
        self.channel_main_url = 'https://www.goesan.go.kr'

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
        'multiple_type': ['post_url', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-9 HYUN
    # html table header index
    table_column_list = ['번호', '교육명', '교육 기간', '정원', '비용', '교육 신청 기간', '상태']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='table_list t_c')

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
                if tmp_td.text.find('데이터가 존재하지 않습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 6:
                if tmp_td.text.find('신청마감') > -1:
                    var['is_going_on'].append(False)
                else:
                    var['is_going_on'].append(True)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_subject', 'post_title'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='table_view')

    var['extra_info'] = [{
        'info_title': '교육상세'
    }]
    var['post_title'] = clean_text(content_info_area.find('th', {'colspan': '4'}).text).strip()

    extra_info_column_list = ['장소', '시간', '비용']

    # 작성자 영역
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '분류':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '신청 기간':
                if tmp_info_value_text.find('~') > -1:
                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:
                        var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
            elif tmp_info_title_text == '교육 기간':
                if tmp_info_value_text.find('~') > -1:
                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:
                        var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date2'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)

            elif tmp_info_title_text == '내용':
                var['post_text'] = clean_text(tmp_info_value_text)
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]


    context_area = content_info_area.find('td', class_='con')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result