from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re
from urllib.parse import urlencode

# 채널 이름 : 중랑

# 타겟 : 보건소 인터넷 신청 접수
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.jungnang.go.kr/health/app/integrateApp/integrateList.do?division=health&programId=integrateApp&menuNo=400152&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.jungnang.go.kr/health/app/integrateApp/select.do?id={post_id}}&division=health&programId=integrateApp&siteId=&menuNo=400152
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '중랑'
        self.post_board_name = '보건소 인터넷 신청 접수'
        self.channel_main_url = 'https://www.jungnang.go.kr'

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
        'multiple_type': ['post_url', 'is_going_on', 'start_date']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-26 HYUN
    # html table header index
    table_column_list = ['NO', '과정명', '신청기간', '모집인원', '상태']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='list_board')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_list_table_bs = post_list_table_bs.find('table')

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

    tmp_page_idx = var['page_count']

    for tmp_post_row in post_row_list:
        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            if idx == 0:
                # 공지사항과 같이 상위 고정
                if tmp_page_idx != 1 and tmp_td.text.strip() == '상시':
                    break

            elif idx == 1:
                if tmp_td.find('a').get('href').find('integrateApp/select.do') < 0:
                    break

                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 2:
                tmp_date_period_str = clean_text(tmp_td.text.strip())
                # 범위기간형식 ex)  2021-12-13 ~ 2021-12-17
                var['start_date'].append(tmp_date_period_str)
            elif idx == 4:
                tmp_column_value = clean_text(tmp_td.text.strip())
                if tmp_column_value == '진행중':
                    var['is_going_on'].append(True)
                else:
                    var['is_going_on'].append(False)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'end_date', 'contact', 'extra_info'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', id='contents')

    contents_title_area = content_info_area.find('p', class_='board_view_tit')
    var['post_title'] = clean_text(contents_title_area.text)

    content_info_area = content_info_area.find('table', class_='viewTable')
    var['extra_info'] = [{
        'info_title':'보건소 신청 상세'
    }]

    extra_info_column_list = ['비용', '장소', '대상', '기간', '신청방식']
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_title_text_removed_space = re.sub('\s+', '', tmp_info_title_text)
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text_removed_space in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text_removed_space)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text_removed_space,
                                                                                 tmp_info_value_text]
            elif tmp_info_title_text == '선정자발표일':
                var['end_date'] = clean_text(tmp_info_value.text.strip())
            elif tmp_info_title_text == '문의전화':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '모집내용':
                var['post_text'] = clean_text(tmp_info_value.text.strip())
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result