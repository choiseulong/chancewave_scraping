from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py
from urllib.parse import urlencode


# 채널 이름 : 양천구

# 타겟 : 행사안내
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/List.do?cbIdx=258&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/View.do?cbIdx=258&bcIdx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '양천구'
        self.post_board_name = '행사안내'
        self.channel_main_url = 'https://www.yangcheon.go.kr'

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
        'multiple_type': ['post_url', 'post_thumbnail', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-31 HYUN
    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='board-card-list2')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find_all('article', class_='post-box')

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:

        thumbnail_area = tmp_post_row.find('div', class_='post-img')
        if thumbnail_area:
            var['post_thumbnail'].append(
                make_absolute_url(in_url=thumbnail_area.find('img').get('src'),
                                  channel_main_url=var['response'].url))
        else:
            var['post_thumbnail'].append('')

        date_area = tmp_post_row.find('p', class_='post-date')
        var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(date_area.text.strip()))

        post_detail_move_button = tmp_post_row.find('p', class_='post-button')
        page_move_function_str = post_detail_move_button.find('a').get('onclick')
        tmp_parameter_str = str_grab(page_move_function_str, 'doBbsFView(', ');')
        parameter_list = eval('[' + tmp_parameter_str + ']')

        tmp_cb_idx = parameter_list[0]
        tmp_bc_idx = parameter_list[1]

        tmp_query_param = {
            'cbIdx': tmp_cb_idx,
            'bcIdx': tmp_bc_idx
        }

        tmp_query = urlencode(tmp_query_param)

        var['post_url'].append(make_absolute_url(
            in_url='/site/yangcheon/ex/bbs/View.do?' + tmp_query,
            channel_main_url=var['response'].url))

    result = merge_var_to_dict(key_list, var)
    print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='basic-view')

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '제목':
                var['post_title'] = str_grab(str(tmp_info_value), "wdigm_title_check('", "')").strip()

    context_area = content_info_area.find('div', class_='view_contents')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result