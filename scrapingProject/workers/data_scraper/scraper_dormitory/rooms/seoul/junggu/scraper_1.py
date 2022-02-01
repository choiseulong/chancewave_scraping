from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 중구

# 타겟 : 행사/축제
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : http://www.junggu.seoul.kr/tour/content.do?cmsid=14987&gotoPage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.junggu.seoul.kr/tour/content.do?cmsid=14987&contentId={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '중구'
        self.post_board_name = '행사/축제'
        self.channel_main_url = 'https://www.junggu.seoul.kr'

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
            self.session.cookies.clear()

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_thumbnail']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', id='contents')
    post_list_table_bs = post_list_table_bs.find('ul', class_='clearfix')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find_all('li')

    for tmp_post_row in post_row_list:

        tmp_post_link = tmp_post_row.find('a').get('href')
        tmp_post_thumbnail_img_url = tmp_post_row.find('img').get('src')

        var['post_url'].append(
            make_absolute_url(
                in_url=tmp_post_link,
                channel_main_url=var['response'].url))

        var['post_thumbnail'].append(
            make_absolute_url(
                in_url=tmp_post_thumbnail_img_url,
                channel_main_url=var['response'].url)
        )

    result = merge_var_to_dict(key_list, var)
    print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'linked_post_url', 'contact', 'start_date', 'end_date'],
        'multiple_type': ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    post_title_area = soup.find('div', class_='imgType_view_title1')
    var['post_title'] = clean_text(post_title_area.find('h2').text)

    content_info_area = soup.find('div', class_='imgType_view_info')
    post_text_area = content_info_area.find('div', class_='info_title')
    var['post_text'] = clean_text(post_text_area.text.strip())

    extra_info_area_list = soup.find('div', class_='info_list').find('ul').find_all('li')
    for tmp_extra_info_area in extra_info_area_list:
        tmp_info_title_text = clean_text(tmp_extra_info_area.find('h5').text).strip()
        tmp_info_value_text = clean_text(tmp_extra_info_area.find('p').text).strip()

        if tmp_info_title_text == '행사일':
            tmp_period_date_list = tmp_info_value_text.split('~')
            var['start_date'] = convert_datetime_string_to_isoformat_datetime(tmp_period_date_list[0])
            var['end_date'] = convert_datetime_string_to_isoformat_datetime(tmp_period_date_list[1])

        elif tmp_info_title_text == '행사장소':
            var['extra_info'].append({
                'info_title': '행사/축제 정보',
                'info_1': [tmp_info_title_text, tmp_info_value_text]
            })
        elif tmp_info_title_text == '홈페이지':
            var['linked_post_url'] = tmp_info_value_text
        elif tmp_info_title_text == '주관사 연락처':
            if not var.get('contact'):
                var['contact'] = tmp_info_value_text
        elif tmp_info_title_text == '주최자 연락처':
            if not var.get('contact'):
                var['contact'] = tmp_info_value_text

    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result