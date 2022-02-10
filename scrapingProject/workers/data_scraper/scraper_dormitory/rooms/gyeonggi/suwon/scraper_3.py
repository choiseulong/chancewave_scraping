from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 수원

# 타겟 : 보건소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://health.suwon.go.kr/board_list.asp?page_code=sub060901&block=1&page={page_count}&strSearch_text=&strSearch_div=&bd_gubn=
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://health.suwon.go.kr/board_view.asp?page_code=sub060901&no={post_id}&bd_gubn=
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '수원'
        self.post_board_name = '보건소식'
        self.channel_main_url = 'https://health.suwon.go.kr/'

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

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'view_count', 'uploader', 'uploaded_time']
    }
    params['response'].encoding = 'UTF8'
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-5 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '첨부', '작성자', '작성일', '조회수']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='board_list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    if post_list_table_bs.find('div', class_='p-empty'):
        print('PAGING END')
        return

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
        for idx, tmp_td in enumerate(tmp_post_row.find_all('th') + tmp_post_row.find_all('td')):

            if idx == 0:
                if tmp_td.text.strip() == '공지' and var['page_count'] != 1:
                    break
            elif idx == 1:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 3:
                var['uploader'].append(clean_text(tmp_td.text).strip())
            elif idx == 4:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 5:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

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
    content_info_area = soup.find('div', class_='board_view')

    title_area = content_info_area.find('div', class_='board_info')

    var['post_title'] = clean_text(title_area.find('h4').text).strip()

    context_area = content_info_area.find('div', class_='substance')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result