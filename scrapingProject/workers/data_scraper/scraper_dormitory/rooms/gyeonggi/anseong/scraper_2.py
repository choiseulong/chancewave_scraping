import json

import js2py

from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlparse, parse_qs, urlsplit, urlencode, ParseResult
from datetime import datetime, timedelta
import requests

# 채널 이름 : 안성

# 타겟 : 행사일정
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.anseong.go.kr/event/program/list/json.do?page={page}&searchSdate={start_date}&searchEdate={end_date}&searchCategory=
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.anseong.go.kr/event/program/popup/detail.do?idx={post_id}
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '안성'
        self.post_board_name = '행사일정'
        self.channel_main_url = 'https://www.anseong.go.kr/'

    def scraping_process(self, channel_code, channel_url, dev):
        super().scraping_process(channel_code, channel_url, dev)
        param_datetime = datetime.now()
        self.page_count = 1

        # 사이트에서 월별 조회, 월의 첫날과 마지막날을 값으로 조회함 ex) 2021-01-01 2021-01-31
        # 데이터가 없어도 12개월 조회 후 종료 하도록 구현

        while True:

            sub_page_no = 1
            # 조회대상 월의 첫일자
            start_date_param_datetime = param_datetime.replace(day=1)
            start_date_param_str = start_date_param_datetime.strftime('%Y-%m-%d')
            # 조회대상 월의 마지막 일자(다음 달의 1일로 변경후 1일 전으로 계산하면 마지막 일자)
            end_date_param_datetime = (param_datetime.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            end_date_param_str = end_date_param_datetime.strftime('%Y-%m-%d')

            print(f'PAGE {self.page_count} : {start_date_param_str} ~ {end_date_param_str}')

            self.channel_url = self.channel_url_frame.format(page=sub_page_no,
                                                             start_date=start_date_param_str,
                                                             end_date=end_date_param_str)

            self.post_list_scraping(post_list_parsing_process, 'get')

            if self.scraping_target:
                self.target_contents_scraping()
                self.collect_data()
                self.mongo.reflect_scraped_data(self.collected_data_list)

            self.page_count += 1
            param_datetime = (param_datetime.replace(day=28) + timedelta(days=4))

            self.session.cookies.clear()

            if self.page_count > 12:
                break

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url']
    }

    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    sub_page_num = 1

    while True:
        print(f'sub page {sub_page_num}')
        tmp_post_data_list = json_data.get('list')
        if tmp_post_data_list is None:
            raise TypeError('CANNOT FIND DATA LIST')
        elif not tmp_post_data_list:
            break

        for tmp_post_data in tmp_post_data_list:
            var['post_url'].append(make_absolute_url(
                in_url='/event/program/popup/detail.do?idx=' + str(tmp_post_data.get('idx')),
                channel_main_url=var['response'].url
            ))

        # 페이징 돌아감
        sub_page_num += 1

        parsed_url = urlparse(var['channel_url'])
        parsed_params = parse_qs(parsed_url.query)
        parsed_params['page'] = sub_page_num
        new_parsed_request_url = ParseResult(scheme=parsed_url.scheme, netloc=parsed_url.hostname,
                                             path=parsed_url.path, params=parsed_url.params, query=urlencode(parsed_params, doseq=True),
                                             fragment=parsed_url.fragment).geturl()
        var['channel_url'] = new_parsed_request_url
        tmp_response = requests.get(var['channel_url'], verify=False)

        if tmp_response.status_code != 200:
            raise TypeError('http error please check')

        try:
            json_data = json.loads(tmp_response.text)
        except json.JSONDecodeError:
            raise TypeError('Can not parse JSON Response')

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_subject', 'post_thumbnail', 'post_content_target', 'post_title', 'start_date', 'end_date',
                        'contact', 'uploader'],
        'multiple_type': ['extra_info']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    var['extra_info'] = [{
        'info_title': '행사 상세'
    }]

    var['post_subject'] = json_data.get('categoryValue')
    var['post_title'] = json_data.get('title')
    var['post_text'] = bs(json_data.get('contents'), 'html.parser').text
    var['contact'] = json_data.get('tel')
    var['start_date'] = convert_datetime_string_to_isoformat_datetime(json_data.get('eventSdate'))
    var['end_date'] = convert_datetime_string_to_isoformat_datetime(json_data.get('eventEdate'))
    var['post_content_target'] = json_data.get('eventTarget')
    var['uploader'] = json_data.get('deptName')

    img_param = {
        'attachId': json_data.get('thumbnail'),
        'fileSn': json_data.get('thumbFileSn'),
        'mode': 'originView'
    }

    tmp_img_param_str = urlencode(img_param)

    var['post_thumbnail'] = make_absolute_url(
        in_url='/common/imgView.do?' + tmp_img_param_str,
        channel_main_url=var['response'].url
    )

    var['extra_info'][0]['info_1'] = ['이용료', json_data.get('eventFee')]
    var['extra_info'][0]['info_2'] = ['장소', json_data.get('eventPlace')]
    var['extra_info'][0]['info_3'] = ['시간', json_data.get('eventTime')]

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result