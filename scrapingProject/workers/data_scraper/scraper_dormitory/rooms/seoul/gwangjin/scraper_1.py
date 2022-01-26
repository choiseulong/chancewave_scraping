from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 광진구

# 타겟 : 마을공동체 공지사항
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.gwangjin.go.kr/portal/bbs/B0000016/list.do?menuNo=200069&pageIndex={}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.sd.go.kr/main/selectBbsNttView.do?bbsNo=183&nttNo={postId}&&pageUnit=10&5
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '광진구'
        self.post_board_name = '마을공동체 공지사항'
        self.channel_main_url = 'https://www.gwangjin.go.kr'

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
        'multiple_type': ['post_url', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-26 HYUN
    # 헤더가 없지만 아래 순서로 나와있음.
    # table_column_list = ['번호', '제목', '부서', '작성일']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='bdList')

    if post_list_table_bs.find('div', class_='nodata'):
        print('PAGING END')
        return

    post_row_list = post_list_table_bs.find('ul').find_all('li')

    for tmp_row_area in post_row_list:
        tmp_title_area = tmp_row_area.find('div', class_='s')
        tmp_post_url = make_absolute_url(in_url=tmp_title_area.find('a').get('href'),
                                         channel_main_url=var['response'].url)
        var['post_url'].append(tmp_post_url)

        tmp_uploaded_time_area = tmp_row_area.find('span', class_='date')
        var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_uploaded_time_area.text.strip()))

    result = merge_var_to_dict(key_list, var)
    print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'view_count', 'uploader', 'contact'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='view')
    var['post_title'] = content_info_area.find('h2').text.strip()
    for tmp_row_area in content_info_area.find_all('dl'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('dt'), tmp_row_area.find_all('dd')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '부서':
                if var.get('uploader'):
                    var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_info_value_text

            elif tmp_info_title_text == '작성자':
                if var.get('uploader'):
                    var['uploader'] = var['uploader'] + ' ' + tmp_info_value_text
                else:
                    var['uploader'] = tmp_info_value_text

            elif tmp_info_title_text == '전화번호':
                var['contact'] = tmp_info_value_text
            elif tmp_info_title_text == '조회수':
                var['view_count'] = extract_numbers_in_text(tmp_info_value_text)

    context_area = content_info_area.find('div', class_='dbData')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result