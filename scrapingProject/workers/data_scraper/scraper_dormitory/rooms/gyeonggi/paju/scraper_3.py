from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 파주시

# 타겟 : 교육프로그램
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://lll.paju.go.kr/user/lll/lecture/BD_lectureList.do?eventClCode=1001&edcMnnstCode=&edcSn=&rcritBgnde=&q_edcMnnstCode=&q_edcClCode=&q_rcritSttusCode=&q_edcReqstMth=&q_edcctAt=&q_area=&q_timeType=&q_edcDayow=&q_edcSj=&q_currPage={page_count}&q_sortName=&q_sortOrder=&q_rowPerPage=10
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://lll.paju.go.kr/user/lll/lecture/BD_lectureView.do?edcMnnstCode=EDC_0001&edcSn={post_id}&eventClCode=1001
    header :
        None
        
    [or]
    
    @post info
    method : GET
    url : https://lib.paju.go.kr/hblib/lectureDetail.do?lectureIdx={post_id}
    header :
        None
'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '파주시'
        self.post_board_name = '교육프로그램'
        self.channel_main_url = 'https://lll.paju.go.kr'

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
        'multiple_type': ['post_url']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-6 HYUN
    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='table')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_list_table_bs = post_list_table_bs.find('table')

    if post_list_table_bs.text.find('게시물이 없습니다') > -1:
        print('PAGING END')
        return

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:
        # jsView('EDC_0002','2022022001') or jsLibraryRequestForm('https://lib.paju.go.kr/jalib/lectureDetail.do?lectureIdx=26787')
        move_link_function_str = tmp_post_row.find('a').get('onclick').strip()
        if move_link_function_str.find('jsLibraryRequestForm') < 0:
            move_link_function_str = str_grab(move_link_function_str, 'jsView(', ');')

            tmp_mnnst_cd = str_grab(move_link_function_str, "'", "',")
            tmp_sn = str_grab(move_link_function_str, "'", "'", index=3)

            query_param = {
                'edcMnnstCode': tmp_mnnst_cd,
                'edcSn': tmp_sn,
                'eventClCode': '1001'
            }
            tmp_query_param_str = urlencode(query_param)

            var['post_url'].append(make_absolute_url(
                in_url='/user/lll/lecture/BD_lectureView.do?' + tmp_query_param_str,
                channel_main_url=var['response'].url
            ))
        else:
            var['post_url'].append(str_grab(move_link_function_str, "jsLibraryRequestForm('", "');"))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'post_subject', 'uploader', 'contact', 'start_date',
                        'end_date', 'start_date2', 'end_date2', 'post_content_target'],
        'multiple_type': ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['extra_info'] = [{
        'info_title': '교육 상세'
    }]
    if var['response'].url.find('lib.paju.go.kr') < 0:
        content_info_area = soup.find('div', class_='article-view')

        content_info_header_area = content_info_area.find('div', class_='article-header')
        title_area = content_info_header_area.find('h1', class_='article-subject')

        var['post_title'] = clean_text(title_area.text).strip()

        content_info_area = content_info_area.find('div', class_='table').find('table')

        extra_info_column_list = ['접수방법', '강사명', '모집인원', '교육요일', '교육시간', '교육비 여부', '교육장소']

        for tmp_row_area in content_info_area.find_all('tr'):
            for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

                tmp_info_title_text = tmp_info_title.text.strip()
                tmp_info_value_text = clean_text(tmp_info_value.text).strip()

                if tmp_info_title_text == '교육분류':
                    var['post_subject'] = tmp_info_value_text
                elif tmp_info_title_text == '교육대상':
                    var['post_content_target'] = tmp_info_value_text
                elif tmp_info_title_text == '모집상태':
                    if tmp_info_value_text.find('모집중') > -1:
                        var['is_going_on'] = True
                    else:
                        var['is_going_on'] = False
                elif tmp_info_title_text == '모집기간':

                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]

                    if date_info_str_list[0]:
                        if len(date_info_str_list) == 2:

                            var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                            var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                        else:
                            var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                            var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])

                elif tmp_info_title_text == '교육기간':

                    tmp_date_period_str = tmp_info_value_text
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if date_info_str_list[0]:
                        if len(date_info_str_list) == 2:

                            var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                            var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                        else:
                            var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                            var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])

                elif tmp_info_title_text == '교육 문의 담당자':
                    var['uploader'] = tmp_info_value_text
                elif tmp_info_title_text == '교육 문의 전화':
                    var['contact'] = tmp_info_value_text
                elif tmp_info_title_text == '교육 내용':
                    var['post_text'] = clean_text(tmp_info_value.text.strip())
                    var['post_image_url'] = search_img_list_in_contents(tmp_info_value, var['response'].url)
                elif tmp_info_title_text in extra_info_column_list:
                    tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                    var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]
    else:
        content_info_area = soup.find('table', class_='board-view')
        extra_info_column_list = ['기관', '시간', '장소', '재료비', '강사명', '접수방법']
        for tmp_row_area in content_info_area.find_all('tr'):
            for tmp_info_title, tmp_info_value in zip(tmp_row_area.find_all('th'), tmp_row_area.find_all('td')):

                tmp_info_title_text = tmp_info_title.text.strip()
                tmp_info_value_text = clean_text(tmp_info_value.text).strip()

                if tmp_info_title_text == '프로그램명':
                    program_status_area = tmp_info_value.find('span')
                    if program_status_area:
                        if program_status_area.text.find('접수중') > -1:
                            var['is_going_on'] = True
                        else:
                            var['is_going_on'] = False
                        program_status_area.decompose()
                    var['post_title'] = tmp_info_value_text
                elif tmp_info_title_text == '접수기간':
                    tmp_date_period_str = tmp_info_value_text
                    tmp_date_period_str = re.sub(r'\([ㄱ-ㅎ가-힣\s\da-zA-Z]+\)', '', tmp_date_period_str)
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:

                        var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                    else:
                        var['start_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])

                elif tmp_info_title_text == '수강기간':
                    tmp_date_period_str = tmp_info_value_text
                    tmp_date_period_str = re.sub(r'\([ㄱ-ㅎ가-힣\s\da-zA-Z]+\)', '', tmp_date_period_str)
                    date_info_str_list = [f.strip() for f in tmp_date_period_str.split('~')]
                    if len(date_info_str_list) == 2:

                        var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[1])
                    else:
                        var['start_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])
                        var['end_date2'] = convert_datetime_string_to_isoformat_datetime(date_info_str_list[0])

                elif tmp_info_title_text == '대상':
                    var['post_content_target'] = tmp_info_value_text
                elif tmp_info_title_text in extra_info_column_list:
                    tmp_extra_info_index = extra_info_column_list.index(tmp_info_title_text)
                    var['extra_info'][0]['info_' + str(tmp_extra_info_index + 1)] = [tmp_info_title_text, tmp_info_value_text]

        context_area = content_info_area.find('td', class_='content')
        var['post_text'] = clean_text(context_area.text.strip())
        var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)
    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result