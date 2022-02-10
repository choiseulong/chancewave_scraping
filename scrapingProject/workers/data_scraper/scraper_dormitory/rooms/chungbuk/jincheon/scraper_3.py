from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 진천군

# 타겟 : 교육/강좌
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : http://www.jincheon.go.kr/site/edu/sub.do?menukey=2836&searchKrwd=&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.jincheon.go.kr/site/edu/sub.do?menukey=2836&mode=view&edu_info_id={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '진천군'
        self.post_board_name = '교육/강좌'
        self.channel_main_url = 'http://www.jincheon.go.kr'

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
        'multiple_type': ['post_url', 'post_subject', 'start_date', 'end_date', 'start_date2', 'end_date2',
                          'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-9 HYUN
    # html table header index
    table_column_list = ['번호', '분류', '강좌명', '접수기간', '교육기간', '교육시간', '모집인원', '접수상태']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='board')

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
                if tmp_td.text.find('데이터가 존재하지 않습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                var['post_subject'].append(tmp_td.text.strip())
            elif idx == 2:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 3:
                tmp_date_period_str = tmp_td.text.strip()
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:
                    var['start_date'].append(datetime.strptime(date_info_str_list[0], '%Y%m%d').isoformat())
                    var['end_date'].append(datetime.strptime(date_info_str_list[1], '%Y%m%d').isoformat())
                else:
                    var['start_date'].append(datetime.strptime(date_info_str_list[0], '%Y%m%d').isoformat())
                    var['end_date'].append(datetime.strptime(date_info_str_list[0], '%Y%m%d').isoformat())
            elif idx == 4:
                tmp_date_period_str = tmp_td.text.strip()
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:
                    var['start_date2'].append(datetime.strptime(date_info_str_list[0], '%Y%m%d').isoformat())
                    var['end_date2'].append(datetime.strptime(date_info_str_list[1], '%Y%m%d').isoformat())
                else:
                    var['start_date2'].append(datetime.strptime(date_info_str_list[0], '%Y%m%d').isoformat())
                    var['end_date2'].append(datetime.strptime(date_info_str_list[0], '%Y%m%d').isoformat())
            elif idx == 7:
                status_text = tmp_td.text.strip()
                if status_text.find('신청마감') > -1:
                    var['is_going_on'].append(False)
                else:
                    var['is_going_on'].append(True)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    content_info_area = soup.find('table', class_='board_view')

    titlea_area = content_info_area.find('th', class_='view_title')
    var['post_title'] = clean_text(titlea_area.text).strip()

    titlea_area.decompose()

    var['extra_info'] = [{
        'info_title': '교육 상세'
    }]

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '강좌 내용':
                var['post_text'] = clean_text(tmp_info_value.text.strip())
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)
            elif tmp_info_title_text == '강좌 장소':
                var['extra_info'][0]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '강좌비':
                var['extra_info'][0]['info_2'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '강좌일&강좌시간':
                lecture_time_str = str_grab(tmp_info_value_text, '(', '')
                if lecture_time_str:
                    lecture_time_str = lecture_time_str[:-1]
                    var['extra_info'][0]['info_3'] = ['강좌시간', lecture_time_str]

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result