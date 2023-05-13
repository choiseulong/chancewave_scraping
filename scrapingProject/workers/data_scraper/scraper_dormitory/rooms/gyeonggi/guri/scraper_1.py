from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# 채널 이름 : 구리

# 타겟 : 문화행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.guri.go.kr/brd/board/1050/L/menu/1670?brdType=L&thisPage={page_count}&searchField=&searchText=
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.guri.go.kr/brd/board/1050/L/menu/1670?brdType=R&thisPage=1&bbIdx={post_id}=&searchField=&searchText=
    header :
        None

'''
sleepSec = 1
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '구리'
        self.post_board_name = '문화행사'
        self.channel_main_url = 'https://www.guri.go.kr'
        print(f'SCRAP {self.channel_name} - {self.post_board_name}')

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

    # def post_list_scraping(self):
    ## post 방식이라면 super().post_list_scraping(postListParsingProcess, 'post', data, sleepSec)
    #     super().post_list_scraping(postListParsingProcess, 'get', sleepSec)

    def target_contents_scraping(self):
        super().target_contents_scraping(post_content_parsing_process, sleepSec)


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'start_date', 'end_date', 'contact', 'post_title', 'post_image_url']
    }
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-1-2 HYUN
    # html table header index
    # 일반적인 테이블 형태 X 테이블 안에 list가 있는 구조
    table_column_list = ['이미지', '담당부서', '전화번호', '행사일', '제목']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='board_wrap_bbs').find('table')
    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:

        for post_info_idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            # 게시물이 없는 경우 & 페이지 끝
            if tmp_td.text.find('현재 게시글이 없습니다.') > -1:
                print('PAGE END')
                return

            if post_info_idx == 0:
                # 사진 영역
                if 'photo' in tmp_td.find('p').get('class'):
                    tmp_img_url = None
                    if tmp_td.find('img').get('src').find('no_img') == -1:
                        tmp_img_url = make_absolute_img_src(img_src=tmp_td.find('img').get('src'),
                                                            channel_main_url=var['channel_main_url'])
                    var['post_image_url'].append(tmp_img_url)
                else:
                    # 사진 영역에 대한 사이트 변경
                    raise ValueError('사진 영역 검증 필요')

            if post_info_idx == 1:

                # TD 내부에 헤더가 li 리스트로 나뉨
                tmp_detail_info_area = tmp_td.find_all('li')[0]
                tmp_title_area = tmp_td.find_all('li')[1]
                tmp_header_title_list = []
                tmp_header_value_list = []
                for detail_info_idx, tmp_detail_info in enumerate(tmp_detail_info_area.find('span').children):
                    if detail_info_idx % 2 == 0:
                        tmp_header_title_list.append(tmp_detail_info.text.strip())
                    else:
                        tmp_header_value_list.append(tmp_detail_info.text.strip())
                tmp_header_title_list = [f for f in tmp_header_title_list if f]
                if len(tmp_header_title_list) != len(tmp_header_value_list):
                    raise ValueError('리스트 정보 영역 확인 필요')

                for header_index, (tmp_header_title, tmp_header_value) in enumerate(zip(tmp_header_title_list, tmp_header_value_list)):
                    if tmp_header_title.split(':')[0].strip() == '전화번호':
                        var['contact'].append(tmp_header_value)
                    elif tmp_header_title.split(':')[0].strip() == '행사일':
                        tmp_start_date = ''
                        tmp_end_date = ''
                        if tmp_header_value:
                            tmp_start_date = convert_datetime_string_to_isoformat_datetime(tmp_header_value)
                            tmp_end_date = convert_datetime_string_to_isoformat_datetime(tmp_header_value)

                        var['start_date'].append(tmp_start_date)
                        var['end_date'].append(tmp_end_date)

                var['post_title'].append(tmp_title_area.text.strip())
                tmp_post_url = tmp_title_area.find('a').get('href')
                tmp_post_url = make_absolute_url(in_url=tmp_post_url, channel_main_url=var['channel_main_url'])
                var['post_url'].append(tmp_post_url)

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'uploader', 'view_count', 'uploaded_time'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='board_wrap_bbs').find('table')

    content_info_header_area = content_info_area.find('thead')
    content_info_header_row_list = content_info_header_area.find_all('tr')

    for tmp_header_row in content_info_header_row_list:
        tmp_column_title_area_list = tmp_header_row.find_all('th')
        tmp_column_value_area_list = tmp_header_row.find_all('td')
        for tmp_column_title_area, tmp_column_value_area in zip(tmp_column_title_area_list, tmp_column_value_area_list):
            tmp_column_title_text = tmp_column_title_area.text.strip()
            tmp_column_value_text = tmp_column_value_area.text.strip()

            if tmp_column_title_text == '담당자':
                if var.get('uploader'):
                    var['uploader'] = var['uploader'] + ' ' + tmp_column_value_text
                else:
                    var['uploader'] = tmp_column_value_text
            elif tmp_column_title_text == '담당부서':
                if var.get('uploader'):
                    var['uploader'] = tmp_column_value_text + ' ' + var['uploader']
                else:
                    var['uploader'] = tmp_column_value_text
            elif tmp_column_title_text == '조회':
                var['view_count'] = extract_numbers_in_text(tmp_column_value_text)
            elif tmp_column_title_text == '작성일':
                var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(tmp_column_value_text)

    content_context_area = content_info_area.find('tbody')
    content_context_area = content_context_area.find('td', class_='context')
    var['post_text'] = clean_text(content_context_area.text)
    var['post_image_url'] = search_img_list_in_contents(content_context_area, var['channel_main_url'])

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result