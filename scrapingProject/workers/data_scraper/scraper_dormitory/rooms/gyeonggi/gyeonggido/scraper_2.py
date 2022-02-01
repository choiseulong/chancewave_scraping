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
    url : https://www.gangdong.go.kr/web/newportal/bbs/b_068/{postId}?cp=1&pageSize=20&sortOrder=BA_REGDATE&sortDirection=DESC&bcId=b_068&baCategory1=U0072&baNotice=false&baCommSelec=false&baOpenDay=true&baUse=true
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '경기도청'
        self.post_board_name = '통합공모'
        self.channel_main_url = 'https://www.gg.go.kr/'

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
        'single_type': ['post_text', 'post_title', 'contact', 'post_content_target', 'uploader', 'start_date', 'end_date', 'start_date2', 'end_date2'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='s-v-board-default')

    header_info_area = content_info_area.find('div', class_='header')

    var['post_title'] = clean_text(header_info_area.find('h2').text).strip()

    header_info_list_area = header_info_area.find('dl')

    for tmp_header_info_area in header_info_list_area.find_all('dd'):
        tmp_header_title = clean_text(tmp_header_info_area.strong.text).strip()
        tmp_header_info_area.strong.decompose()
        tmp_header_value = clean_text(tmp_header_info_area.text).strip()


    content_info_area = content_info_area.find('table')

    for tmp_row_area in content_info_area.find_all('tr'):
        for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

            tmp_info_title_text = tmp_info_title.text.strip()
            tmp_info_value_text = tmp_info_value.text.strip()

            if tmp_info_title_text == '제목':
                var['post_title'] = tmp_info_value_text
            elif tmp_info_title_text == '전화번호':
                var['contact'] = tmp_info_value_text

    context_area = content_info_area.find('td', class_='board_con')

    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result