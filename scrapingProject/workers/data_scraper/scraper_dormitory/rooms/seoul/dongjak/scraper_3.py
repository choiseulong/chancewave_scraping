from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py
from urllib.parse import urlencode


# 채널 이름 : 동작구

# 타겟 : 문화행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.dongjak.go.kr/portal/bbs/B0000173/list.do?menuNo=201030&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.dongjak.go.kr/portal/bbs/B0000173/view.do?nttId=10587876&menuNo=201030&pageIndex={}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '동작구'
        self.post_board_name = '문화행사'
        self.channel_main_url = 'https://www.dongjak.go.kr'

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

    # 2022-1-31 HYUN


    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='gallery2')
    post_list_table_bs = post_list_table_bs.find('ul', class_='row-fluid')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find_all('li', recursive=False)

    if not post_row_list:
        print('PAGING END')
        return

    for tmp_post_row in post_row_list:
        var['post_url'].append(make_absolute_url(
            in_url=tmp_post_row.find('a').get('href'),
            channel_main_url=var['response'].url))
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
        'single_type': ['post_text', 'post_subject', 'post_content_target', 'post_title', 'uploader', 'contact', 'start_date', 'end_date'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='contentData')
    var['extra_info'] = [{
        'info_title':'행사 상세'
    }]
    var['post_title'] = clean_text(content_info_area.find('p', class_='subject').text).strip()

    header_area = content_info_area.find('div', class_='desc')

    for tmp_info_title, tmp_info_value in zip(header_area.find_all('dt'), header_area.find_all('dd')):

        tmp_info_title_text = tmp_info_title.text.strip()
        tmp_info_value_text = tmp_info_value.text.strip()

        if tmp_info_title_text == '구분':
            var['post_subject'] = tmp_info_value_text
        elif tmp_info_title_text == '대상':
            var['post_content_target'] = tmp_info_value_text
        elif tmp_info_title_text == '행사일':
            tmp_date_period_str = tmp_info_value_text
            date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
            var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
            var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
        elif tmp_info_title_text == '전화문의':
            # 담당자 / 연락처 포맷 <<<
            if tmp_info_value_text.find('/') > -1:
                uploader_contact_info_list = [f.strip() for f in tmp_info_value_text.split('/')]

                if var.get('uploader'):
                    var['uploader'] = var['uploader'] + ' ' + uploader_contact_info_list[0]
                else:
                    var['uploader'] = uploader_contact_info_list[0]
                var['contact'] = uploader_contact_info_list[1]
            # 담당자 이름 안나올 경우 연락처만 있다고 가정.
            else:
                var['contact'] = tmp_info_value_text

        elif tmp_info_title_text == '담당부서':
            if var.get('uploader'):
                var['uploader'] = tmp_info_value_text + ' ' + var['uploader']
            else:
                var['uploader'] = tmp_info_value_text

        elif tmp_info_title_text == '신청방법':
            var['extra_info'][0]['info_1'] = [tmp_info_title_text, tmp_info_value_text]
        elif tmp_info_title_text == '장소':
            var['extra_info'][0]['info_2'] = [tmp_info_title_text, tmp_info_value_text]

    context_area = content_info_area.find('div', id='tabContent01')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result