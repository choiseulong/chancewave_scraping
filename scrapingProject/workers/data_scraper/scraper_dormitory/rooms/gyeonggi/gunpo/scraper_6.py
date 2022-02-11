from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 군포

# 타겟 : 행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.gunpo.go.kr/portal/edcClturEventList.do?key=1008282&bbsNo=684&searchCtgry=%%ED%%96%%89%%EC%%82%%AC/%%EC%%B6%%95%%EC%%A0%%9C&pageUnit=10&searchCnd=all&searchKrwd=&integrDeptCode=&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.gunpo.go.kr/portal/edcClturEventView.do?key=1008282&bbsNo=684&nttNo={post_id}&searchCtgry=%%ED%%96%%89%%EC%%82%%AC/%%EC%%B6%%95%%EC%%A0%%9C
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '군포'
        self.post_board_name = '행사'
        self.channel_main_url = 'https://www.gunpo.go.kr'

    def scraping_process(self, channel_code, channel_url, dev, full_channel_code):
        super().scraping_process(channel_code, channel_url, dev, full_channel_code)

        self.session = set_headers(self.session)
        self.session.get('https://www.gunpo.go.kr/portal/edcClturEventList.do?key=1008282&bbsNo=684&searchCtgry=%%ED%%96%%89%%EC%%82%%AC/%%EC%%B6%%95%%EC%%A0%%9C', verify=False)
        self.session.get(self.channel_url_frame.format(self.page_count), verify=False)

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

    # 2022-2-4 HYUN

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='contents_box')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find_all('div', class_='list_item')

    for tmp_post_row in post_row_list:
        var['post_url'].append(make_absolute_url(
            in_url=tmp_post_row.find('a', class_='cont_box').get('href'),
            channel_main_url=var['response'].url
        ))
        thumbnail_img = tmp_post_row.find('span', class_='img_box').find('img')
        if thumbnail_img.get('alt') == 'no image':
            var['post_thumbnail'].append('')
        else:
            var['post_thumbnail'].append(make_absolute_url(
                in_url=thumbnail_img.get('src'),
                channel_main_url=var['response'].url
            ))

    result = merge_var_to_dict(key_list, var)

    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'post_subject', 'uploader', 'uploaded_time', 'view_count',
                        'start_date', 'end_date', 'post_content_target'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('table', class_='bbs_default')
    var['extra_info'] = [{
        'info_title': '문화 상세'
    }]

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = clean_text(tmp_info_value.text).strip()

            if tmp_info_title_text == '분류':
                var['post_subject'] = tmp_info_value_text
            elif tmp_info_title_text == '제목':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '행사기간':
                date_info_str_list = [f.strip() for f in tmp_info_value_text.split('~')]
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
            elif tmp_info_title_text == '담당자':
                if var.get('uploader') and var.get('uploader') != tmp_info_value_text:
                    var['uploader'] = var['uploader'] + ' ' + tmp_info_value_text
                else:
                    var['uploader'] = tmp_info_value_text

            elif tmp_info_title_text == '담당부서':
                if var.get('uploader') and var.get('uploader') != tmp_info_value_text:
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_info_value_text
            elif tmp_info_title_text == '등록일':
                var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(tmp_info_value_text)
            elif tmp_info_title_text == '조회':
                var['view_count'] = extract_numbers_in_text(tmp_info_value_text)
            elif tmp_info_title_text == '대상':
                var['post_content_target'] = tmp_info_value_text
            elif tmp_info_title_text == '장소':
                var['extra_info'][0]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
            elif tmp_info_title_text == '상세내용':
                var['post_text'] = tmp_info_value_text
                var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result