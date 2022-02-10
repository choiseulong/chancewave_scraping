from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 오산시

# 타겟 : 현재공연
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.osan.go.kr/arts/program/list.do?cCategory=0&mId=0101010000&page={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.osan.go.kr/arts/program/view.do?mId=0101010000&idx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '오산시'
        self.post_board_name = '현재공연'
        self.channel_main_url = 'https://www.osan.go.kr'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.session = set_headers(self.session)
        self.page_count = 1

        already_scrap_param_list = []

        while True:

            filtered_scrap_list = []
            print(f'PAGE {self.page_count}')

            self.channel_url = self.channel_url_frame.format(self.page_count)

            self.post_list_scraping(post_list_parsing_process, 'get')

            for tmp_new_scrap_target_obj in self.scraping_target:

                if tmp_new_scrap_target_obj['post_url'] not in already_scrap_param_list:
                    filtered_scrap_list.append(tmp_new_scrap_target_obj)
                    already_scrap_param_list.append(tmp_new_scrap_target_obj['post_url'])

            self.scraping_target = filtered_scrap_list
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
        'multiple_type': ['post_url']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '내용']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='table_perform')

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
        move_page_js_function_text = tmp_post_row.find('a').get('onclick')
        page_idx = str_grab(move_page_js_function_text, "view('", "');")

        var['post_url'].append(make_absolute_url(
            in_url='/arts/program/view.do?mId=0101010000&idx=' + str(page_idx),
            channel_main_url=var['response'].url))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_subject', 'post_title', 'post_thumbnail', 'linked_post_url',
                        'start_date', 'end_date', 'contact'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    var['extra_info'] = [{
        'info_title': '공연 상세'
    }]

    content_area = soup.find('div', class_='content')

    var['post_thumbnail'] = make_absolute_url(
        in_url=content_area.find('p', id='poster_view').find('img').get('src'),
        channel_main_url=var['response'].url
    )

    header_area = content_area.find('div', class_='detail_top')
    title_area = header_area.find('dt')

    subject_area = title_area.find('span', class_='showSort')
    if subject_area:
        var['post_subject'] = clean_text(subject_area.text)
        subject_area.decompose()

    var['post_title'] = clean_text(title_area.text).strip()

    extra_info_column_list = ['공연 시간', '관람시간', '장소', '관렴연령', '입장료', '할인정보', '주최', '주관']

    for tmp_row_area in content_area.find('dd').find('ul').find_all('li', recursive=False):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('span', class_='th'), tmp_row_area.find_all('span', class_='td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '공연기간':
                tmp_date_period_str = tmp_info_value_text
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:

                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
            elif tmp_info_title_text == '문의처':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '예매링크':
                var['linked_post_url'] = tmp_info_value.find('a').get('href')
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]

    post_imgae_area = content_area.find('div', id='galleryThum')
    var['post_image_url'] = search_img_list_in_contents(post_imgae_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result