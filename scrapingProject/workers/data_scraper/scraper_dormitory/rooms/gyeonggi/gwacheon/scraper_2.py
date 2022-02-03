import js2py

from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlparse, parse_qs, urlsplit, urlencode, ParseResult
from datetime import datetime, timedelta
# 채널 이름 : 과천시

# 타겟 : 문화행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url :  https://www.gccity.go.kr/portal/bbs/list.do?ptIdx=111&mId=0301010000
    header :
        None
    body :
        None

'''
'''
    @post info
    method : GET
    url :  https://www.gccity.go.kr/dept/bbs/view.do?mId=0102000000&bIdx={postId}&ptIdx=241
    header :
        None
    body :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '과천시'
        self.post_board_name = '중소기업 및 소상공인 지원'
        self.channel_main_url = 'https://www.gccity.go.kr'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        param_datetime = datetime.now()
        self.page_count = 1

        # 2022년 11월 -> 2022년 12월 식으로 년월 단위로 페이지가 넘어감.
        # 기간에 포함된 행사는 다른 년월에 중복해서 나오므로 중복 제거하는 로직 포함
        already_scrap_param_list = []

        while True:

            print(f'PAGE {self.page_count}')
            sub_page_no = 1
            start_date_param_datetime = param_datetime.replace(day=1)
            start_date_param_str = start_date_param_datetime.strftime('%Y-%m-%d')
            end_date_param_datetime = (param_datetime.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            end_date_param_str = end_date_param_datetime.strftime('%Y-%m-%d')

            self.channel_url = self.channel_url_frame.format(page=sub_page_no,
                                                             start_date=start_date_param_str,
                                                             end_date=end_date_param_str)

            self.post_list_scraping(post_list_parsing_process, 'get')

            if self.scraping_target:
                # self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)
                self.page_count += 1
                param_datetime = (param_datetime.replace(day=28) + timedelta(days=4))
            else:
                break

            self.session.cookies.clear()


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_url_can_use', 'post_title', 'extra_info', 'post_text', 'post_image_url', 'extra_info']
    }

    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    sub_page_num = 1

    while True:

        tmp_post_data_list = json_data.get('result')
        if tmp_post_data_list is None:
            raise TypeError('CANNOT FIND DATA LIST')
        elif not tmp_post_data_list:
            return
        total_page = json_data.get('totalPage')
        for tmp_post_data in tmp_post_data_list:
            tmp_image_url_list = []
            tmp_extra_info = {
                'info_title': '문화행사 상세'
            }
            var['post_title'].append(tmp_post_data['title'])
            var['post_text'].append(clean_text(tmp_post_data['contents']))
            var['post_url'].append(var['channel_url'])
            var['post_url_can_use'].append(False)
            var['post_content_target'] = tmp_post_data['target']
            var['contact'].append(tmp_post_data['tel'])
            var['uploader'].append(tmp_post_data['supervisor'])
            var['start_date'].append(convert_datetime_string_to_isoformat_datetime(tmp_post_data['eventStartDate']))
            var['end_date'].append(convert_datetime_string_to_isoformat_datetime(tmp_post_data['eventEndDate']))
            if tmp_post_data['fileList']:
                for tmp_file in tmp_post_data['fileList']:
                    tmp_image_url_list.append(
                        make_absolute_url(in_url='/common/imgView.do?attachId=' + tmp_file.get('attachId') +
                                                 '&fileSn=' + tmp_file.get('fileSn') + '&mode=ratio',
                                          channel_main_url=var['response'].url
                                          ))
            var['post_image_url'].append(tmp_image_url_list)
            tmp_extra_info['info_1'] = ['장소', tmp_post_data['eventPlace']]
            tmp_extra_info['info_2'] = ['주소', tmp_post_data['addr']]
            tmp_extra_info['info_3'] = ['요금', tmp_post_data['fee']]
            var['extra_info'].append([tmp_extra_info])

        # 페이징 돌아감
        sub_page_num += 1
        parsed_url = urlparse(var['channel_url'])
        parsed_params = parse_qs(parsed_url.query)
        parsed_params['page'] = sub_page_num
        new_parsed_request_url = ParseResult(scheme=parsed_url.scheme, netloc=parsed_url.hostname,
                                             path=parsed_url.path, params=parsed_url.params, query=urlencode(parsed_params),
                                             fragment=parsed_url.fragment)
        var['channel_url'] = new_parsed_request_url

        print(json_data)



    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result
