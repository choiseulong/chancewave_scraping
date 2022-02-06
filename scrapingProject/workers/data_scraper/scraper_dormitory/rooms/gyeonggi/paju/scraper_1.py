from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 파주시

# 타겟 : 문화행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://tour.paju.go.kr/user/link/cultural/BD_index.do?q_currPage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://tour.paju.go.kr/user/link/cultural/BD_selectCulturalView.do?cultMstSn={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '파주시'
        self.post_board_name = '문화행사'
        self.channel_main_url = 'https://tour.paju.go.kr/'

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
        'multiple_type': ['post_url', 'post_thumbnail']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('ul', class_='event_list')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    if post_list_table_bs.text.find('게시물이 없습니다') > -1:
        print('PAGING END')
        return

    post_row_list = post_list_table_bs.find_all('li', recursive=False)

    for tmp_post_row in post_row_list:

        post_idx = tmp_post_row.find('a').get('onclick').strip()
        post_idx = str_grab(post_idx, 'jsCulturalView(', ');')

        var['post_url'].append(make_absolute_url(
            in_url='BD_selectCulturalView.do?cultMstSn=' + post_idx,
            channel_main_url=var['response'].url
        ))

        var['post_thumbnail'].append(make_absolute_url(
            in_url=tmp_post_row.find('img').get('src'),
            channel_main_url=var['response'].url
        ))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'post_subject', 'post_content_target', 'start_date', 'end_date',
                        'contact'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    var['post_title'] = clean_text(soup.find('div', class_='sub_title').text).strip()
    content_info_area = soup.find('li', class_='event_table_info')

    content_info_header_area = content_info_area.find('table')

    var['extra_info'] = [{
        'info_title': '행사 상세'
    }]

    extra_info_column_list = ['행사지역', '관람연령', '행사시간', '행사장소', '참가비', '행사주최', '행사주관']

    for tmp_row_area in content_info_header_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '행사분류':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '이용자':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text == '문의하기':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '행사기간':
                tmp_date_period_str = tmp_info_value_text
                date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                if len(date_info_str_list) == 2:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                else:
                    var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                    var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
            elif tmp_info_title_text in extra_info_column_list:
                tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                var['extra_info'][0]['info_' + str(tmp_extra_info_index)] = [tmp_info_title_text, tmp_info_value_text]

    context_area = soup.find('div', class_='detail_view_area')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result