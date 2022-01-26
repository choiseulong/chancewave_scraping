from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 중랑

# 타겟 : 공연안내 및 예약
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.jungnang.go.kr/portal/app/integrateApp/integrateList.do?division=event&programId=integrateApp&menuNo=200383&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.jungnang.go.kr/portal/app/event/select.do?id={post_id}&programId=event&division=event&menuNo=200383
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '중랑'
        self.post_board_name = '공연안내 및 예약'
        self.channel_main_url = 'https://www.jungnang.go.kr'

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
        'multiple_type': ['post_url', 'post_subject', 'start_date', 'end_date', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-26 HYUN
    # html table header index
    table_column_list = ['번호', '구분', '제목', '신청기간', '처리현황']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='table_wrap')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_list_table_bs = post_list_table_bs.find('table', class_='inc_head')

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
        # 첫번째, 게시물 '번호'가 th이므로 td 인덱스에서 1개 제외
        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):


            if idx == 0:
                var['post_subject'].append(clean_text(tmp_td.text))
            elif idx == 1:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 2:
                tmp_date_period_str = clean_text(tmp_td.text)
                date_str_list = tmp_date_period_str.split('~')
                date_str_list = [f.strip() for f in date_str_list]
                if len(date_str_list) == 2:
                    var['start_date'].append(convert_datetime_string_to_isoformat_datetime(date_str_list[0]))
                    var['end_date'].append(convert_datetime_string_to_isoformat_datetime(date_str_list[1]))
                else:
                    var['start_date'].append(tmp_date_period_str)
            elif idx == 3:
                if tmp_td.find('img', {'alt':'마감'}):
                    var['is_going_on'].append(False)
                else:
                    var['is_going_on'].append(True)

    result = merge_var_to_dict(key_list, var)
    print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        # start_date2 : 공연시작 시간
        'single_type': ['post_text', 'post_title', 'start_date2'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['extra_info'] = []
    content_info_area = soup.find('div', class_='txt_box')
    var['post_title'] = content_info_area.find('h2').text.strip()

    content_info_area = content_info_area.find('div', class_='half_txt')
    content_info_area = content_info_area.find('ul')

    for tmp_row_area in content_info_area.find_all('li'):
        column_title = tmp_row_area.em.text.strip()
        tmp_row_area.em.decompose()
        column_value = clean_text(tmp_row_area.text).replace(': ', '').strip()

        if column_title == '공연시간':
            var['start_date2'] = convert_datetime_string_to_isoformat_datetime(column_value)
        elif column_title == '관람료':
            var['extra_info'].append({
                '관람료': column_value
            })
        elif column_title == '공연장소':
            var['extra_info'].append({
                '공연장소': column_value
            })

    poster_area = soup.find('div', class_='half_box')
    poster_area = poster_area.find('div', class_='half_img')

    var['post_image_url'] = search_img_list_in_contents(poster_area, var['response'].url)

    context_area = soup.select_one('div.gray_bg_box.img_box.line')
    var['post_text'] = clean_text(context_area.text.strip())

    if var['post_image_url'] is None:
        var['post_image_url'] = []

    var['post_image_url'].extend(search_img_list_in_contents(context_area, var['response'].url))

    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result