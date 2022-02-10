from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py
from urllib.parse import urlencode


# 채널 이름 : 관악구

# 타겟 : 행정접수
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.gwanak.go.kr/site/gwanak/ex/reservation/re00401.do?riIdx=RI001440&pageIndex={page_count}&riType=E&searchCondition2=all
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gwanak.go.kr/site/gwanak/ex/reservation/re00403.do?riIdx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '관악구'
        self.post_board_name = '행정접수'
        self.channel_main_url = 'https://www.gwanak.go.kr'

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
        'multiple_type': ['post_url']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-31 HYUN
    # html table header index
    table_column_list = ['번호', '행사명', '담당부서', '접수기간', '접수상태']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='board')
    post_list_table_bs = post_list_table_bs.find('table', class_='list')

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
            raise ('List Column Index Change')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                if tmp_td.text.find('등록된 게시글이 없습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                page_move_function_str = tmp_td.find('a').get('href')
                tmp_parameter_str = str_grab(page_move_function_str, "doReservationSiteEventView('", "');")
                tmp_parameter_str = clean_text(tmp_parameter_str)
                var['post_url'].append(make_absolute_url(
                    in_url='/site/gwanak/ex/reservation/re00403.do?riIdx=' + tmp_parameter_str,
                    channel_main_url=var['response'].url
                ))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)

    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'is_going_on', 'post_title', 'uploader', 'contact', 'start_date', 'end_date', 'post_thumbnail'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', id='contents')
    var['extra_info'] = [{
        'info_title':'강좌/행사 상세'
    }]
    var['post_title'] = clean_text(content_info_area.find('span', class_='name').text).strip()
    if content_info_area.select('span.status.ia'):
        var['is_going_on'] = True
    else:
        var['is_going_on'] = False

    content_info_area = content_info_area.find('table', class_='info-table')

    var['post_thumbnail'] = ''
    thumbnail_ara = soup.find('div', class_='photo')
    if thumbnail_ara:
        var['post_thumbnail'] = make_absolute_url(
            in_url=thumbnail_ara.find('img').get('src'),
            channel_main_url=var['response'].url
        )
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '접수기간':
                if tmp_info_value_text.find('~') > -1:
                    # 기간
                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:
                        var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                    else:
                        var['start_date'] = ''
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                else:
                    # 하루
                    one_day_date_str = clean_text(tmp_info_value_text).strip()
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)

            elif tmp_info_title_text == '전화문의':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '담당부서':
                var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '장소':
                var['extra_info'][0]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '모집인원':
                var['extra_info'][0]['info_2'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '참가비':
                var['extra_info'][0]['info_3'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '접수방법':
                var['extra_info'][0]['info_4'] = [tmp_info_title_text, tmp_info_value_text]

    context_area = soup.find('div', class_='app-detail').find('div', class_='detail-wrap')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)

    return result