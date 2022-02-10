from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 군포

# 타겟 : 교육/강좌
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.gunpo.go.kr/portal/webEdcLctreList.do?key=1008274&searchCnd=all&searchKrwd=&searchStartDate=&searchEndDate=&searchLctreLclas=&searchRceptSttus=&pageUnit=10&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gunpo.go.kr/portal/edcLctreView.do?key=1008274&searchLctreKey={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '군포'
        self.post_board_name = '교육/강좌'
        self.channel_main_url = 'https://www.gunpo.go.kr'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)

        self.session = set_headers(self.session)
        self.session.get('https://www.gunpo.go.kr/portal/webEdcLctreList.do?key=1008274&rep=1', verify=False)
        self.session.get(self.channel_url_frame.format(self.page_count), verify=False)

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
        'multiple_type': ['post_url', 'post_title']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-4 HYUN
    # html table header index
    table_column_list = ['상태', '교육명/장소', '대상', '신청/교육기간', '정원', '선별방법 수강료', '신청방법']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='p-table')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    if soup.find('div', class_='p-empty'):
        print('PAGING END')
        return

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('thead')
    # 테이블 칼럼 리스트
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')

    # 테이블 컬럼명 검증 로직
    for column_idx, tmp_header_column in enumerate(post_list_table_header_list_bs):
        if table_column_list[column_idx] != clean_text(tmp_header_column.text).strip():
            print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {clean_text(tmp_header_column.text).strip()}')
            raise('List Column Index Change')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                if tmp_td.text == '공지':
                    break
            elif idx == 1:

                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
                var['post_title'].append(clean_text(tmp_td.find('a').text).strip())

    result = merge_var_to_dict(key_list, var)

    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_subject', 'start_date', 'end_date', 'post_content_target',
                        'contact', 'is_going_on'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='p-table')
    var['extra_info'] = [{
        'info_title': '교육강좌 상세'
    }]

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '강좌영역':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '강좌상태':
                if tmp_info_value_text.find('모집마감') > -1:
                    var['is_going_on'] = False
                else:
                    var['is_going_on'] = True

            elif tmp_info_title_text == '신청기간':
                [f.decompose() for f in tmp_info_value.find_all('p')]
                tmp_date_period_str = clean_text(tmp_info_value.text).strip()
                tmp_date_period_str = re.sub(r'\([ㄱ-ㅎ가-힣\s\da-zA-Z]+\)', '', tmp_date_period_str)
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])

            elif tmp_info_title_text == '교육기간':
                tmp_date_period_str = clean_text(tmp_info_value.text).strip()
                tmp_date_period_str = re.sub(r'\([ㄱ-ㅎ가-힣\s\da-zA-Z]+\)', '', tmp_date_period_str)
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])


            elif tmp_info_title_text == '강의시간':
                var['extra_info'][0]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '수강료':
                var['extra_info'][0]['info_2'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '강의장소':
                var['extra_info'][0]['info_3'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '수강대상':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text == '주최':
                var['extra_info'][0]['info_4'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '문의':
                var['contact'] = clean_text(tmp_info_value.text.strip())

    context_area = soup.find('div', class_='p-accordion__content')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result