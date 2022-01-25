from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 종로

# 타겟 : 민원신청 통합신청
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.jongno.go.kr/portal/app/integrateApp/list.do?menuNo=388366&pageIndex={pageCount}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.jongno.go.kr/portal/app/integrateApp/view.do?menuId=388366&menuNo=388366&id={postId}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '종로'
        self.post_board_name = '민원신청 통합신청'
        self.channel_main_url = 'https://www.jongno.go.kr'

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
        'multiple_type': ['post_url', 'is_going_on', 'start_date']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-25 HYUN
    # html table header index
    table_column_list = ['번호', '프로그램명', '신청기간', '접수현황', '결과확인']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='respon-table1')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('ul', class_='respon-th')
    # 테이블 칼럼 리스트
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('li')

    # 테이블 컬럼명 검증 로직
    for column_idx, tmp_header_column in enumerate(post_list_table_header_list_bs):
        if table_column_list[column_idx] != tmp_header_column.text.strip():
            print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {tmp_header_column.text.strip()}')
            raise('List Column Index Change')

    post_row_list = post_list_table_bs.find_all('ul', class_='respon-td')

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('li')):
            tmp_column_title = tmp_td.span.text.strip()
            tmp_column_value = tmp_td.em.text.strip()

            if tmp_column_title == '프로그램명':
                page_move_function_str = tmp_td.find('a').get('href')
                tmp_post_id = str_grab(page_move_function_str, ",'", "')", from_back=True)

                var['post_url'].append(make_absolute_url(
                    in_url='/portal/app/integrateApp/view.do?menuId=388366&menuNo=388366&id=' + tmp_post_id,
                    channel_main_url=var['response'].url))

            elif tmp_column_title == '접수현황':
                if tmp_td.find('img').get('alt') == '진행중':
                    var['is_going_on'].append(True)
                else:
                    var['is_going_on'].append(False)

            elif tmp_column_title == '신청기간':
                # 범위기간형식 ex)  2021-12-13 09:00 ~ 2021-12-17 18:00
                if tmp_column_value.find('~') > -1:
                    date_list = [f.strip() for f in tmp_column_value.split('~') if f.strip()]
                    var['start_date'].append(' '.join(date_list))
                else:
                    var['start_date'].append(clean_text(tmp_column_value))

    result = merge_var_to_dict(key_list, var)
    print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'post_content_target', 'end_date', 'contact', 'extra_info'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='board_view')
    content_info_area = content_info_area.find('table')

    var['post_title'] = soup.find('h4', class_='bu_t1').text.strip()
    var['extra_info'] = []

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '선정자발표':
                try:
                    # 날짜 형식인 경우 datetime으로 저장
                    tmp_address_date = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
                    var['end_date'] = tmp_address_date
                except Exception:
                    # 날짜 형식 아닌 경우 문자열로 저장 ex) '상시발표'
                    var['end_date'] = tmp_info_value_text
            elif tmp_info_title_text == '신청대상':
                var['post_content_target'] = tmp_info_value_text

            elif tmp_info_title_text == '문의전화':
                var['contact'] = clean_text(tmp_info_value_text)

            elif tmp_info_title_text in ['모집내용', '공모내용/참여방법']:
                var['post_text'] = clean_text(tmp_info_value_text)
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)
            elif tmp_info_title_text in ['선정방식', '교육비용', '장 소']:
                var['extra_info'].append({
                    tmp_info_title_text: tmp_info_value_text
                })

    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result