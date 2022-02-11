from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from unicodedata import normalize

# 채널 이름 : 청주시

# 타겟 : 평생학습관 공지사항
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.cheongju.go.kr/www/selectBbsNttList.do?key=280&bbsNo=510&searchCtgry=&pageUnit=10&searchCnd=all&searchKrwd=&integrDeptCode=000100101&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.cheongju.go.kr/www/selectBbsNttView.do?key=280&bbsNo=510&nttNo={post_id}&searchCtgry=&searchCnd=all&searchKrwd=&pageIndex=2&integrDeptCode=000100101
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '청주시'
        self.post_board_name = '평생학습관 공지사항'
        self.channel_main_url = 'https://lll.cheongju.go.kr/'

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
        'multiple_type': ['post_url']
    }

    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    # 2022-2-8 HYUN
    total_page_num = json_data['paging']['totalPages']

    if total_page_num == var['page_count']:
        print('PAGING END')
        return
    for tmp_post in json_data['dataList']:
        var['post_url'].append(make_absolute_url(
            in_url='/board/view?bbsConf.seq=1&increase=true&bbsNttSeq=' + str(tmp_post['seq']),
            channel_main_url=var['response'].url
        ))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):

    target_key_info = {
        'single_type': ['post_text', 'uploader', 'view_count', 'uploaded_time'],
        'multiple_type': ['post_image_url']
    }

    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    post_data = json_data['data']
    var['post_title'] = post_data['nttSj']
    context_area = bs(post_data['nttCn'], 'html.parser')
    var['post_text'] = clean_text(context_area.text)
    var['post_image_url'] = search_img_list_in_contents(context_area, var['channel_main_url'])
    var['view_count'] = post_data['readCo']
    var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(post_data['registDt'])
    var['uploader'] = post_data['changeUser']['name']

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result