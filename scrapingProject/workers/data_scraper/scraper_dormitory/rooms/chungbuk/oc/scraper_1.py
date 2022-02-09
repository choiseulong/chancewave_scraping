from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 옥천군

# 타겟 : 정보화교육 신청
# 중단 시점 : 마지막 페이지 도달시

# HTTP Requests
'''
    @post list

    method : GET
    url : https://www.oc.go.kr/ocmc/selectTnCnteduProgrmListU.do?sc1=%EC%A0%95%EB%B3%B4%ED%99%94%EA%B5%90%EC%9C%A1&sc2=%EB%AF%B8%EB%94%94%EC%96%B4%EC%84%BC%ED%84%B0&sc5=%EC%A0%95%EC%83%81&callScreen=viewTnCnteduProgrm&key=1762&cpn={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.oc.go.kr/ocmc/viewTnCnteduProgrmU.do?progrmNo={post_id}&sc1=%EC%A0%95%EB%B3%B4%ED%99%94%EA%B5%90%EC%9C%A1&sc2=%EB%AF%B8%EB%94%94%EC%96%B4%EC%84%BC%ED%84%B0&sc5=%EC%A0%95%EC%83%81&callScreen=viewTnCnteduProgrm&key=1762
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '옥천군'
        self.post_board_name = '정보화교육 신청'
        self.channel_main_url = 'https://www.oc.go.kr/'

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
        'multiple_type': ['post_url']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-9 HYUN

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('ul', class_='photo_list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    for tmp_row in post_list_table_bs.find_all('li', recursive=False):
        var['post_url'].append(
            make_absolute_url(
                in_url=tmp_row.find('a', class_='photo_title').get('href'),
                channel_main_url=var['response'].url
            )
        )


    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'start_date', 'end_date', 'start_date2', 'end_date2', 'post_content_target'],
        'multiple_type': ['post_image_url', 'extra_info']
    }

    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    if soup.text.find('로그인 정보가 없습니다') > -1:
        return None

    contents_area = soup.find('div', class_='box_wrap')
    title_area = contents_area.find('h3')
    status_area = title_area.find('span', class_='status_label')

    if status_area:
        if status_area.text.find('교육중') > -1:
            var['is_going_on'] = True
        else:
            var['is_going_on'] = False
        status_area.decompose()

    var['post_title'] = clean_text(title_area.text).strip()
    var['extra_info'] = [{
        'info_title': '교육 상세'
    }]

    extra_info_column_list = ['교육시간', '수강료', '교육장소']

    for tmp_header_area in contents_area.find('ul').find_all('li', recursive=False):
        header_title_area = tmp_header_area.find('strong', class_='temp_subject')
        tmp_info_title_text = header_title_area.text.strip()

        header_title_area.decompose()
        tmp_info_value_text = clean_text(tmp_header_area.text).strip()

        if tmp_info_title_text == '신청기간':
            tmp_date_period_str = tmp_info_value_text
            date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
            if len(date_info_str_list) == 2:

                var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
            else:
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])

        elif tmp_info_title_text == '교육기간':
            tmp_date_period_str = tmp_info_value_text
            date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
            if len(date_info_str_list) == 2:

                var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
            else:
                var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])

        elif tmp_info_title_text == '교육대상':
            var['post_content_target'] = tmp_info_value_text

        elif tmp_info_title_text in extra_info_column_list:
            tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
            var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]

    context_area = soup.find('p', class_='box_text')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result