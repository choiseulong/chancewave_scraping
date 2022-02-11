from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 평택시

# 타겟 : 전체행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.pyeongtaek.go.kr/pyeongtaek/bbs/list.do?ptIdx=41&mId=0401010000&bIdx=
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.pyeongtaek.go.kr/pyeongtaek/bbs/view.do?mId=0401010000&bIdx={postId}&ptIdx=41
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '평택시'
        self.post_board_name = '전체행사'
        self.channel_main_url = 'https://www.pyeongtaek.go.kr'

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
        'multiple_type': ['post_url', 'start_date', 'end_date']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # html table header index
    table_column_list = ['번호', '구분', '분야', '행사명', '행사기간', '장소', '상태', '조회수']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='tableSt_list')

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
            raise ('List Column Index Change')

    # 게시물 리스트 테이블 영역

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            if idx == 3:
                post_move_function_str = tmp_td.find('a').get('onclick')
                post_idx = str_grab(post_move_function_str, "view_proc('", "');")
                var['post_url'].append(
                    make_absolute_url(
                        in_url='/alrimi/festival/view.do?mId=0101000000&idx=' + post_idx,
                        channel_main_url=var['response'].url
                    )
                )
            elif idx == 4:
                if tmp_td.text.find('~') > -1:
                    # 기간
                    tmp_date_period_str = clean_text(tmp_td.text).strip()
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    var['start_date'].append(convert_datetime_string_to_isoformat_datetime(date_info_str_list[0]))
                    var['end_date'].append(convert_datetime_string_to_isoformat_datetime(date_info_str_list[1]))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_thumbnail', 'post_text', 'post_title', 'post_subject', 'contact', 'post_content_target',
                        'linked_post_url'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='detail_top')

    content_header_info_area = content_info_area.find('dl')

    var['post_title'] = clean_text(content_header_info_area.find('p', id='titleTxtKo').text).strip()
    var['post_thumbnail'] = make_absolute_url(
        in_url=content_info_area.find('p', id='poster_view').find('img').get('src'),
        channel_main_url=var['response'].url
    )

    content_header_info_area_list = content_header_info_area.find('div', class_='infoBox').find_all('ul', recursive=False)
    var['extra_info'] = [{
        'info_title': '행사 상세'
    }]

    extra_info_column_list = ['시간', '장소', '주관/주최', '이용료']

    for content_header_info_area in content_header_info_area_list:
        for tmp_row_area in content_header_info_area.find_all('li', recursive=False):
            tmp_info_title = tmp_row_area.find('span', class_='th')
            tmp_info_value = tmp_row_area.find('span', class_='td')

            tmp_info_title_text = tmp_info_title.text.strip()
            if not tmp_info_value:
                continue
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '분야(장르)':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '문의':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '이용연령':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text == '홈페이지':
                var['linked_post_url'] = tmp_info_value.find('a').get('href')
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]

    context_area = soup.find('span', id='koContent')

    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result