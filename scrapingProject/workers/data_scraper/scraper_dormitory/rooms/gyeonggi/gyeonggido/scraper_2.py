from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 경기도청

# 타겟 : 통합공모
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.gangdong.go.kr/web/newportal/bbs/b_068/list?cp={page_count}&pageSize=20&bcId=b_068&baCategory1=U0072
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gg.go.kr/bbs/boardView.do?bIdx={post_id}&bsIdx=731&menuId=2916
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '경기도청'
        self.post_board_name = '통합공모'
        self.channel_main_url = 'https://www.gg.go.kr/'

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
        'multiple_type': ['post_url', 'post_thumbnail']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-1 HYUN

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('ul', id='contest-list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_area_list = post_list_table_bs.find_all('li')

    for tmp_post_area in post_area_list:
        var['post_url'].append(tmp_post_area.find('a').get('href'))
        var['post_thumbnail'].append(tmp_post_area.find('span', class_='thumnails').find('img').get('src'))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'contact', 'post_content_target', 'uploader', 'start_date',
                        'uploaded_time', 'end_date', 'start_date2', 'end_date2', 'view_count', 'is_going_on'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='s-v-board-default')

    header_info_area = content_info_area.find('div', class_='header')
    var['extra_info'] = [{
        'info_title':'공모상세'
    }]
    var['post_title'] = clean_text(header_info_area.find('h2').text).strip()

    header_info_list_area = header_info_area.find('dl')

    for tmp_header_info_area in header_info_list_area.find_all('dd'):
        tmp_header_title = clean_text(tmp_header_info_area.strong.text).strip()
        tmp_header_info_area.strong.decompose()
        tmp_header_value = clean_text(tmp_header_info_area.text).strip()

        if tmp_header_title == '작성자':
            var['uploader'] = tmp_header_value
        elif tmp_header_title == '작성일':
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(tmp_header_value)
        elif tmp_header_title == '조회':
            var['view_count'] = extract_numbers_in_text(tmp_header_value)

    header_info_area = content_info_area.find('div', class_='equitable_box')
    header_info_area = header_info_area.find('div')
    for tmp_header_info_sub_area in header_info_area.find_all('div', recursive=False):
        for tmp_info_area in tmp_header_info_sub_area.find('div').find_all('div'):
            tmp_info_title = clean_text(tmp_info_area.span.text).strip()
            tmp_info_area.span.decompose()
            tmp_info_value = clean_text(tmp_info_area.text).strip()

            if tmp_info_title == '응모대상':
                var['post_content_target'] = tmp_info_value
            elif tmp_info_title == '접수기간':
                if tmp_info_value.find('~') > -1:
                    # 기간
                    tmp_date_period_str = tmp_info_value
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:
                        var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                    else:
                        var['start_date'] = ''
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                else:
                    # 하루
                    one_day_date_str = clean_text(tmp_info_value).strip()
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)

            elif tmp_info_title == '진행상황':
                if tmp_info_value != '접수중':
                    var['is_going_on'] = True
                else:
                    var['is_going_on'] = False
            elif tmp_info_title == '문의':
                var['contact'] = tmp_info_value
            elif tmp_info_title == '공모주제':
                var['extra_info'][0]['info_1'] =[tmp_info_title, tmp_info_value]
            elif tmp_info_title == '응모분야':
                var['extra_info'][0]['info_2'] = [tmp_info_title, tmp_info_value]
            elif tmp_info_title == '접수방법':
                var['extra_info'][0]['info_3'] = [tmp_info_title, tmp_info_value]
            elif tmp_info_title == '시상규모':
                var['extra_info'][0]['info_4'] = [tmp_info_title, tmp_info_value]
            elif tmp_info_title == '심사방법':
                var['extra_info'][0]['info_5'] = [tmp_info_title, tmp_info_value]
            elif tmp_info_title == '주최·주관':
                var['extra_info'][0]['info_6'] = [tmp_info_title, tmp_info_value]
            elif tmp_info_title == '최종결과':
                try:
                    if tmp_info_value.find('~') > -1:
                        # 기간
                        tmp_date_period_str = tmp_info_value
                        date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                        if len(date_info_str_list) == 2:
                            var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                            var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                        else:
                            var['start_date2'] = ''
                            var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    else:
                        # 하루
                        one_day_date_str = clean_text(tmp_info_value).strip()
                        var['start_date2'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
                        var['end_date2'] = convert_datetime_string_to_isoformat_datetime(one_day_date_str)
                except Exception:
                    var['start_date2'] = clean_text(tmp_info_value).strip()
                    var['end_date2'] = clean_text(tmp_info_value).strip()

    context_area = content_info_area.find('div', class_='text-center').find('div', class_='item')

    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result