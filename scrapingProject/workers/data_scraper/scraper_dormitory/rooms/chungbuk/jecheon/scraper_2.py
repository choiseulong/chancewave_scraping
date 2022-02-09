from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py
from urllib.parse import urlencode


# 채널 이름 : 제천

# 타겟 : 행사 홍보
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.jecheon.go.kr/www/selectBbsNttList.do?key=3553&id=&&bbsNo=1153&searchCtgry=&pageUnit=10&searchCnd=all&searchKrwd=&integrDeptCode=&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.jecheon.go.kr/www/selectBbsNttView.do?key=128&id=&&bbsNo=24&nttNo={}&searchCtgry=&searchCnd=&searchKrwd=&pageIndex=1&integrDeptCode=
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '제천'
        self.post_board_name = '행사 홍보'
        self.channel_main_url = 'https://www.jecheon.go.kr'

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

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('ul', class_='p-media-list')

    post_row_list = post_list_table_bs.find_all('li', class_='p-media')

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:
        var['post_url'].append(
            make_absolute_url(
                in_url=tmp_post_row.find('a').get('href'),
                channel_main_url=var['response'].url))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'start_date', 'end_date', 'post_subject', 'uploader', 'view_count',
                        'linked_post_url'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='bbs__view')

    content_info_area = content_info_area.find('table', class_='p-table')

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '메인 제목':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '시작일':
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
            elif tmp_info_title_text == '종료일':
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
            elif tmp_info_title_text == '카테고리':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '작성자':
                var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '조회수':
                var['view_count'] = extract_numbers_in_text(tmp_info_value_text)
            elif tmp_info_title_text == '링크':
                var['linked_post_url'] = tmp_info_value_text

    context_area = content_info_area.find('td', class_='bbs_content')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result