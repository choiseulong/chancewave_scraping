from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 동두천

# 타겟 : 평생학습관 강좌
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://edu.ddc.go.kr/ddcedu/courseList.do?key=19&pageUnit=10&srcStatus=&srcYear=&srcQuarter=&srcTitle=&srcCategory=&srcEdu=246&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://edu.ddc.go.kr/ddcedu/courseView.do?key=19&course={post_id}&srcYear=&srcQuarter=
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '동두천'
        self.post_board_name = '평생학습관 강좌'
        self.channel_main_url = 'https://edu.ddc.go.kr/'

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
        'multiple_type': ['post_url', 'post_title', 'post_subject', 'post_content_target', 'is_going_on']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-5 HYUN
    # html table header index
    table_column_list = ['번호', '분야', '대상', '강좌명', '강사', '교육시간', '접수인원/정원', '수강신청']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='bbs_default_list')

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
                if tmp_td.text.find('등록된 게시물이 없습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                var['post_subject'].append(clean_text(tmp_td.text).strip())
            elif idx == 2:
                var['post_content_target'].append(clean_text(tmp_td.text).strip())
            elif idx == 3:
                page_move_function_str = tmp_td.find('a').get('href').strip()
                var['post_url'].append(make_absolute_url(
                    in_url=page_move_function_str,
                    channel_main_url=var['response'].url))
                var['post_title'].append(clean_text(tmp_td.text).strip())
            elif idx == 7:
                if clean_text(tmp_td.text).strip().find('접수 마감') > -1:
                    var['is_going_on'].append(False)
                else:
                    var['is_going_on'].append(True)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'contact', 'linked_post_url', 'start_date', 'end_date'],
        'multiple_type': ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    var['extra_info'] =[
        {
            'info_title':'강좌상세'
        },
        {
            'info_title':'교육기관 상세'
        }]
    # 내용 테이블별 나눔
    for tmp_content_info_area in soup.find_all('table', class_='bbs_basic'):
        tmp_sector_name = None
        tmp_sector_name_area = tmp_content_info_area.find('th', {'colspan': [2, 4]})
        if tmp_sector_name_area:
            tmp_sector_name = tmp_sector_name_area.text
            tmp_sector_name = clean_text(tmp_sector_name).strip()
            tmp_sector_name_area.decompose()

        for tmp_row_area in tmp_content_info_area.find_all('tr'):
            for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):
                tmp_info_title_text = clean_text(tmp_info_title.text).strip()
                tmp_info_value_text = clean_text(tmp_info_value.text).strip()

                if tmp_sector_name == '강좌정보':
                    if tmp_info_title_text == '교육기간':
                        tmp_date_period_str = tmp_info_value_text
                        date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                        if len(date_info_str_list) == 2:

                            var['start_date'] = datetime.strptime(date_info_str_list[0], '%Y년 %m월 %d일').isoformat()
                            var['end_date'] = datetime.strptime(date_info_str_list[1], '%Y년 %m월 %d일').isoformat()
                        else:
                            var['start_date'] = datetime.strptime(date_info_str_list[0], '%Y년 %m월 %d일').isoformat()
                            var['end_date'] = datetime.strptime(date_info_str_list[0], '%Y년 %m월 %d일').isoformat()
                    elif tmp_info_title_text == '기수별':
                        var['extra_info'][0]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '교육장소':
                        var['extra_info'][0]['info_2'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '강사명':
                        var['extra_info'][0]['info_3'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '강의시간':
                        var['extra_info'][0]['info_4'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '수강료':
                        var['extra_info'][0]['info_5'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '재료비':
                        var['extra_info'][0]['info_6'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '접수장소':
                        var['extra_info'][0]['info_7'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '신청방법':
                        var['extra_info'][0]['info_8'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '학습내용':
                        var['post_text'] = tmp_info_value_text

                elif tmp_sector_name == '교육기관 정보':
                    if tmp_info_title_text == '연락처':
                        var['contact'] = tmp_info_value_text
                    elif tmp_info_title_text == '분류':
                        var['extra_info'][1]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '담당자':
                        var['extra_info'][1]['info_2'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '주소':
                        var['extra_info'][1]['info_3'] = [tmp_info_title_text, tmp_info_value_text]
                    elif tmp_info_title_text == '홈페이지':
                        var['linked_post_url'] = tmp_info_value_text

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result