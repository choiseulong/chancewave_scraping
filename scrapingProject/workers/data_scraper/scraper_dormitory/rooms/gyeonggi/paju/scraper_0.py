from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from urllib.parse import urlencode

# 채널 이름 : 파주시

# 타겟 : 새소식
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url = https://www.paju.go.kr/user/board/BD_board.list.do?seq=&bbsCd=2001&pageType=&showSummaryYn=N&delDesc=&q_ctgCd=&q_parentCtgCd=&q_searchKeyType=&q_searchVal=&q_currPage={page_count}&q_sortName=&q_sortOrder=&q_rowPerPage=8
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://agri.paju.go.kr/user/board/BD_board.view.do?seq={postId}&bbsCd=2001&showSummaryYn=N&q_ctgCd=1018
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '파주시'
        self.post_board_name = '새소식'
        self.channel_main_url = 'https://www.paju.go.kr'

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

    # 2022-1-13 HYUN
    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('ul', class_='summary-list')

    if post_list_table_bs.text.find('게시물이 없습니다') > -1:
        print('PAGING END')
        return

    # # 테이블 컬럼 영역
    # post_list_table_header_area_bs = post_list_table_bs.find('thead')
    # # 테이블 칼럼 리스트
    # post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')
    #
    # # 테이블 컬럼명 검증 로직
    # for column_idx, tmp_header_column in enumerate(post_list_table_header_list_bs):
    #     if table_column_list[column_idx] != tmp_header_column.text.strip():
    #         print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {tmp_header_column.text.strip()}')
    #         raise('List Column Index Change')

    post_row_list = post_list_table_bs.find_all('div', class_='summary-body')

    for tmp_post_row in post_row_list:
        # tmp_post_text_area = tmp_post_row.find('div', class_='content-area')

        move_link_function_str = tmp_post_row.find('a').get('onclick').strip()
        move_link_function_str = str_grab(move_link_function_str, 'jsNewView(', '; return')

        tmp_bbsCd = str_grab(move_link_function_str, "'", "',")
        tmp_seq = str_grab(move_link_function_str, "'", "',", index=3)

        query_param = {
            'bbsCd': tmp_bbsCd,
            'seq': tmp_seq,
            'q_ctgCd': '1018'
        }
        tmp_query_param_str = urlencode(query_param)

        var['post_url'].append(make_absolute_url(
            in_url='./BD_board.view.do', channel_main_url=var['response'].url
        ) + '?' + tmp_query_param_str)

    result = merge_var_to_dict(key_list, var)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'view_count', 'post_subject', 'uploader', 'uploaded_time'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='article-view')

    content_info_header_area = content_info_area.find('div', class_='article-header')
    title_area = content_info_header_area.find('h1', class_='article-subject')

    # 주제 분류
    if title_area.find('span'):
        var['post_subject'] = title_area.find('span').text.strip()
        title_area.find('span').decompose()
    else:
        var['post_subject'] = ''

    var['post_title'] = title_area.text.strip()

    content_info_list = content_info_header_area.find('ul', class_='info-list').find_all('li')
    for tmp_content_info in content_info_list:
        if tmp_content_info.find('span').text.strip() == '조회수':
            tmp_content_info.find('span').decompose()
            var['view_count'] = extract_numbers_in_text(tmp_content_info.text.strip())
        elif tmp_content_info.find('span').text.strip() == '작성일':
            tmp_content_info.find('span').decompose()
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(tmp_content_info.text.strip())
        elif tmp_content_info.find('span').text.strip() == '담당부서':
            tmp_content_info.find('span').decompose()
            if var['uploader']:
                var['uploader'] = tmp_content_info.text.strip() + ' ' + var['uploader']
            else:
                var['uploader'] = tmp_content_info.text.strip()
        elif tmp_content_info.find('span').text.strip() == '담당자':
            tmp_content_info.find('span').decompose()
            if var['uploader']:
                var['uploader'] = var['uploader'] + ' ' + tmp_content_info.text.strip()
            else:
                var['uploader'] = tmp_content_info.text.strip()

    context_area = content_info_area.find('div', class_='article-conetnt')
    var['post_text'] = clean_text(context_area.text.strip())
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    return result