from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 성남시

# 타겟 : 행사/강좌/공모
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.seongnam.go.kr/city/1000053/30003/bbsList.do?currentPage={page_count}&searchSelect=title&searchAddSelect=&searchAddWord=&searchIngState=A&searchCategory=&orderByNm=idx+DESC&idx=&subTabIdx=&type=list
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.seongnam.go.kr/city/1000053/30003/bbsView.do?idx={post_id}
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '성남시'
        self.post_board_name = '행사/강좌/공모'
        self.channel_main_url = 'https://www.seongnam.go.kr'

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

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-7 HYUN
    # html table header index
    table_column_list = ['번호', '분류', '행사명', '행사기간', '상태', '대상']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='board-list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    if post_list_table_bs.find('td', class_='empty'):
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

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                pass
                # if tmp_td.text.strip() == '공지':
                #     break
            elif idx == 2:

                page_idx_area_str = tmp_td.find('a').get('onclick')
                page_idx = str_grab(page_idx_area_str, "dataView('", "');")
                var['post_url'].append(make_absolute_url(
                    in_url='/city/1000053/30003/bbsView.do?idx=' + page_idx,
                    channel_main_url=var['response'].url))
            elif idx == 4:
                if tmp_td.text.find('진행중') > -1:
                    var['is_going_on'].append(True)
                else:
                    var['is_going_on'].append(False)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'uploader', 'post_subject', 'contact', 'start_date', 'end_date',
                        'uploaded_time', 'post_content_target'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    var['extra_info'] = [{
        'info_title': '내용 상세'
    }]
    extra_info_column_list = ['행사시간']
    content_info_area = soup.find('table', class_='board-view')
    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '행사명':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '분류':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '행사(접수)기간':
                tmp_date_period_str = tmp_info_value_text
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:

                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
            elif tmp_info_title_text == '등록일':
                var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
            elif tmp_info_title_text == '연락처':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '대상':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text == '작성자':
                if var.get('uploader'):
                    var['uploader'] = var['uploader'] + ' ' + tmp_info_value_text
                else:
                    var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '작성부서':
                if var.get('uploader'):
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]

    context_area = content_info_area.find('td', class_='content')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result