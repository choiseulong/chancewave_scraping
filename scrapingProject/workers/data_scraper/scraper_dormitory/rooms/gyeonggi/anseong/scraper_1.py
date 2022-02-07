from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 안성

# 타겟 : 모집공고
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.anseong.go.kr/portal/recruitment/notice/list.do?mId=0205030100&currentPageNo={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.anseong.go.kr/portal/recruitment/notice/view.do?mId=0205030100&idx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '안성'
        self.post_board_name = '모집공고'
        self.channel_main_url = 'https://www.anseong.go.kr'

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

    # 2022-2-5 HYUN

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('ul', class_='recruitment-list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find_all('li', recursive=False)

    for tmp_post_row in post_row_list:
        page_link_a_tag = tmp_post_row.find('a', {'data-button': 'view'})
        page_index = page_link_a_tag.get('data-idx')
        var['post_url'].append(
            make_absolute_url(
                in_url='/portal/recruitment/notice/view.do?mId=0205030100&idx=' + page_index,
                channel_main_url=var['response'].url
        ))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'start_date', 'end_date', 'contact', 'is_going_on'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='tableSt_view')

    var['extra_info'] = [{
        'info_title': '모집 상세'
    }]

    extra_info_column_list = ['선정방식']

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '문의처':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '공고명':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '접수기간':
                tmp_date_period_str = tmp_info_value_text
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:

                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])

            elif tmp_info_title_text == '공고내용':
                var['post_text'] = tmp_info_value_text
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)

            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]

            elif tmp_info_title_text == '모집현황':
                if tmp_info_value_text.find('모집중') > -1:
                    var['is_going_on'] = True
                else:
                    var['is_going_on'] = False

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result