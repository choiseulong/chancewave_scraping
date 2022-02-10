from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from datetime import timedelta
from urllib.parse import urlencode, urlparse, parse_qs

# 채널 이름 : 성동구

# 타겟 : 행사/접수
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.sd.go.kr/main/selectTnOnlineRceptListU.do?sc3={년월(ex:202201 - 2022년 1월)}&key=4169
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.sd.go.kr/main/viewTnOnlineRceptU.do?progrmNo=49&key=4169
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '성동구'
        self.post_board_name = '행사/접수'
        self.channel_main_url = 'https://www.sd.go.kr'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        self.session = set_headers(self.session)
        param_datetime = datetime.now()
        self.page_count = 1

        # 2022년 11월 -> 2022년 12월 식으로 년월 단위로 페이지가 넘어감.
        # 기간에 포함된 행사는 다른 년월에 중복해서 나오므로 중복 제거하는 로직 포함
        already_scrap_param_list = []

        while True:
            print(f'PAGE {self.page_count}')
            tmp_year_month_str = param_datetime.strftime('%Y%m')

            self.channel_url = self.channel_url_frame.format(tmp_year_month_str)
            self.post_list_scraping(post_list_parsing_process, 'get')

            # 중복된 게시물 제거한, 스크래핑 대상 URL
            filtered_scrap_list = []

            for tmp_new_scrap_target_obj in self.scraping_target:
                tmp_url_params = parse_qs(urlparse(tmp_new_scrap_target_obj.get('post_url')).query)
                tmp_new_scrap_param_str = 'progrmNo='+tmp_url_params['progrmNo'][0] + '&key=' + tmp_url_params['key'][0]
                if tmp_new_scrap_param_str not in already_scrap_param_list:
                    filtered_scrap_list.append(tmp_new_scrap_target_obj)
                    already_scrap_param_list.append(tmp_new_scrap_param_str)

            self.scraping_target = filtered_scrap_list

            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
                param_datetime = (param_datetime.replace(day=28) + timedelta(days=4))
            else:
                break
            self.session.cookies.clear()

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'start_date', 'end_date', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-26 HYUN
    # html table header index
    table_column_list = ['번호', '프로그램명', '모집인원', '접수기간', '진행상황', '인원현황']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='bbs__list')
    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')
    post_list_table_bs = post_list_table_bs.find('table', class_='p-table')

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
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 3:
                tmp_regist_period_str = clean_text(tmp_td.text).strip()
                regist_period_date_list = [f.strip() for f in tmp_regist_period_str.split('~')]
                var['start_date'].append(datetime.strptime(regist_period_date_list[0], '%Y.%m.%d %H시').isoformat())
                var['end_date'].append(datetime.strptime(regist_period_date_list[1], '%Y.%m.%d %H시').isoformat())
            elif idx == 4:
                if clean_text(tmp_td.text).strip() == '접수중':
                    var['is_going_on'].append(True)
                else:
                    var['is_going_on'].append(False)

    result = merge_var_to_dict(key_list, var)
    print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    content_info_area = soup.find('div', class_='bbs__view')
    content_info_area = content_info_area.find('table', class_='p-table')
    var['extra_info'] = []

    var['post_title'] = clean_text(content_info_area.find('td', class_='p-table__subject_text'))
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '모집인원':
                var['extra_info'].append({
                    tmp_info_title_text: tmp_info_value_text
                })
            elif tmp_info_title_text == '프로그램내용':
                var['post_text'] = clean_text(tmp_info_value.text.strip())
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result