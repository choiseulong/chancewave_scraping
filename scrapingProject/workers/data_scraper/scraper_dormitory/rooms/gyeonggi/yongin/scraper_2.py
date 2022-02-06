from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 용인시

# 타겟 : 문화행사/공연
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.yongin.go.kr/user/web/newsApi/BD_selectNewsApiList.do?q_searchVal=&q_currPage={page_count}&q_sortName=&q_sortOrder=&
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.yongin.go.kr/user/web/newsApi/BD_selectNewsApi.do?ca_code={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '용인시'
        self.post_board_name = '문화행사/공연'
        self.channel_main_url = 'https://www.yongin.go.kr'

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
    post_list_table_bs = soup.find('div', id='photo_list_02')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find('ul').find_all('li', recursive=False)

    for tmp_post_row in post_row_list:
        if tmp_post_row.text.find('등록된 게시물이 없습니다') > -1:
            return
        thumbnail_area = tmp_post_row.find('p', class_='thum_s')
        var['post_thumbnail'].append(make_absolute_url(
            in_url=thumbnail_area.find('img').get('src'),
            channel_main_url=var['response'].url
        ))

        var['post_url'].append(make_absolute_url(
            in_url=tmp_post_row.find('dt', class_='btitle').find('a').get('href'),
            channel_main_url=var['response'].url))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'post_subject', 'start_date', 'end_date', 'contact'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='t_view').find('table')
    var['extra_info'] = [{'info_title':'공연 상세'}]
    var['post_title'] = clean_text(content_info_area.find('td', class_='title').text).strip()

    header_area = content_info_area.find('ul', class_='tview_list')
    for tmp_row_area in header_area.find_all('li'):
        tmp_info_text = clean_text(tmp_row_area.text).strip()

        tmp_info_title_text = str_grab(tmp_info_text, '', ':').strip()
        tmp_info_value_text = str_grab(tmp_info_text, ':', '').strip()

        if tmp_info_title_text == '분 류':
            var['post_subject'] = tmp_info_value_text
        elif tmp_info_title_text == '문 의 처':
            var['contact'] = tmp_info_value_text
        elif tmp_info_title_text == '분 류':
            var['post_subject'] = tmp_info_value_text
        elif tmp_info_title_text == '행사기간':
            tmp_date_period_str = tmp_info_value_text
            date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]

            if len(date_info_str_list) == 2:
                var['start_date'] = datetime.strptime(date_info_str_list[0], '%Y년 %m월 %d일')
                var['end_date'] = datetime.strptime(date_info_str_list[1], '%Y년 %m월 %d일')
            else:
                var['start_date'] = datetime.strptime(date_info_str_list[0], '%Y년 %m월 %d일')
                var['end_date'] = datetime.strptime(date_info_str_list[0], '%Y년 %m월 %d일')

        elif tmp_info_title_text == '장소':
            var['extra_info'][0]['info_1'] = ['장소', tmp_info_value_text]
    context_area = content_info_area.find('div', class_='boxstyle01')

    var['post_text'] = clean_text(context_area.text).strip()
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result