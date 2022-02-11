from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 강동구

# 타겟 : 행사/접수
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.songpa.go.kr/www/selectBbsNttList.do?bbsNo=98&&pageUnit=10&key=2783&searchAditfield4=&searchAditfield5=&viewBgnde=&searchAditfield1=&searchAditfield2=&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gangdong.go.kr/web/koRenew_1/reserve/uiRenewView.do?reserveid={post_id}&menuId=tpl:16312
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '강동구'
        self.post_board_name = '행사/접수'
        self.channel_main_url = 'https://www.gangdong.go.kr'

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
            self.session.cookies.clear()

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_subject',
                          'start_date', 'end_date', 'start_date2', 'end_date2', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-19 HYUN
    # html table header index
    table_column_list = ['번호', '분야', '교육·행사명', '접수기간', '교육·행사 일시', '진행상태', '접수인원']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='table01')
    post_list_table_bs = post_list_table_bs.find('table')

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
                if tmp_td.text.find('등록된 게시글이 없습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                var['post_subject'].append(tmp_td.text.strip())
            elif idx == 2:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 3:
                tmp_info_value_text = clean_text(tmp_td.text).strip()
                if tmp_info_value_text.find('~') > -1:
                    # 기간
                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    var['start_date'].append(convert_datetime_string_to_isoformat_datetime(date_info_str_list[0]))
                    var['end_date'].append(convert_datetime_string_to_isoformat_datetime(date_info_str_list[1]))
                else:
                    # 하루
                    one_day_date_str = clean_text(tmp_info_value_text).strip()
                    var['start_date'].append(convert_datetime_string_to_isoformat_datetime(one_day_date_str))
                    var['end_date'].append(convert_datetime_string_to_isoformat_datetime(one_day_date_str))
            elif idx == 4:
                tmp_info_value_text = clean_text(tmp_td.text).strip()
                if tmp_info_value_text.find('~') > -1:
                    # 기간
                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    var['start_date2'].append(convert_datetime_string_to_isoformat_datetime(date_info_str_list[0]))
                    var['end_date2'].append(convert_datetime_string_to_isoformat_datetime(date_info_str_list[1]))
                else:
                    # 하루
                    one_day_date_str = clean_text(tmp_info_value_text).strip()
                    var['start_date2'].append(convert_datetime_string_to_isoformat_datetime(one_day_date_str))
                    var['end_date2'].append(convert_datetime_string_to_isoformat_datetime(one_day_date_str))

            elif idx == 5:
                if tmp_td.text.strip() != '마감':
                    var['is_going_on'].append(True)
                else:
                    var['is_going_on'].append(False)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='table_view')
    content_info_area = content_info_area.find('table')

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '행사제목':
                var['post_title'] = tmp_info_value_text

    context_area = content_info_area.find_all('tr').pop()

    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result