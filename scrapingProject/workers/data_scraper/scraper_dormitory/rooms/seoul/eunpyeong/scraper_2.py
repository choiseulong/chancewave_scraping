from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode, parse_qs, urlparse

# 채널 이름 : 은평

# 타겟 : 강좌/교육
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.ep.go.kr/www/selectBbsNttList.do?key=744&bbsNo=42&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.ep.go.kr/CmsWeb/viewPage.req?idx=PG0000001131&boardDataId={postId}&CP0000000002_BO0000000087_Action=boardView&CP0000000002_BO0000000087_ViewName=board/BoardView
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '은평'
        self.post_board_name = '강좌/교육'
        self.channel_main_url = 'https://www.ep.go.kr'

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
        'multiple_type': ['post_url']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-10 HYUN
    # html table header index
    table_column_list = ['강좌명', '번호', '담당부서', '신청기간', '교육기간', '등록일']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='bbs__list')
    post_list_table_bs = soup.find('table', class_='p-table')

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

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'uploader', 'start_date', 'end_date', 'contact', 'view_count', 'post_content_target'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='bbs__view')
    title_area = content_info_area.find('span', class_='p-table__subject_text')
    var['post_title'] = clean_text(title_area.text).strip()

    content_info_area = content_info_area.find('table')

    header_info_area = content_info_area.find('div', class_='p-author__info')
    uploader_area = header_info_area.find('em', text='작성자 :').nextSibling
    view_count_area = header_info_area.find('em', text='조회 :').find_next_sibling('span')
    var['uploader'] = clean_text(uploader_area.text).strip()
    var['view_count'] = extract_numbers_in_text(view_count_area.text)

    var['extra_info'] = [{
        'info_title':'강좌/교육 상세'
    }]

    extra_info_column_list = ['수강료', '교육장소', '신청방법']

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '담당부서':
                if var.get('uploader'):
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '신청기간':
                var['start_date'] = tmp_info_value_text
            elif tmp_info_title_text == '교육기간':
                var['end_date'] = tmp_info_value_text
            elif tmp_info_title_text == '문의':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '교육대상':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index)] = [tmp_info_title_text, tmp_info_value_text]

    context_area = soup.find('td', class_='p-table__content')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result