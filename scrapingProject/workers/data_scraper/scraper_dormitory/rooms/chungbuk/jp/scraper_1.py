from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 증평군

# 타겟 : 문화예술공연
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list

    method : GET
    url : https://www.jp.go.kr/kor/cop/bbs/BBSMSTR_000000000151/selectBoardList.do?bbsId=BBSMSTR_000000000151&nttId=0&bbsTyCode=BBST05&bbsAttrbCode=BBSA03&pdfview_at=&authFlag=&mno=sitemap_12&searchCnd=0&searchWrd=&pageIndex={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : https://www.jp.go.kr/kor/cop/bbs/BBSMSTR_000000000151/selectBoardArticle.do?nttId={post_id}&kind=&mno=sitemap_12&pageIndex=1&searchCnd=0&searchWrd=
    header :
        None

'''
sleepSec = 0
isUpdate = True


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '증평군'
        self.post_board_name = '문화예술공연'
        self.channel_main_url = 'https://www.jp.go.kr'

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
        'multiple_type': ['post_url', 'view_count', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-9 HYUN
    # html table header index
    table_column_list = ['순번', '제목', '부서명', '등록일', '조회', '첨부']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='basic_table')

    if not post_list_table_bs:
        raise TypeError('CANNOT FIND LIST TABLE')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('thead')
    # 테이블 칼럼 리스트
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')

    # 테이블 컬럼명 검증 로직
    for column_idx, tmp_header_column in enumerate(post_list_table_header_list_bs):
        if table_column_list[column_idx] != tmp_header_column.text.strip():
            print(f'IDX {column_idx} ERROR - {table_column_list[column_idx]} is {tmp_header_column.text.strip()}')
            raise('List Column Index Change')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')
    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):

            if idx == 0:
                if tmp_td.text.find('데이터가 존재하지 않습니다') > -1:
                    print('PAGING END')
                    return
            elif idx == 1:
                var['post_url'].append(make_absolute_url(
                    in_url=tmp_td.find('a').get('href'),
                    channel_main_url=var['response'].url))
            elif idx == 3:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 4:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'post_title', 'uploader', 'contact'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    content_info_area = soup.find('div', class_='bbs_detail')

    titlea_area = content_info_area.find('div', class_='bbs_detail_tit').find('h2')
    var['post_title'] = clean_text(titlea_area.text).strip()

    header_info_area = content_info_area.find('li', class_='part')
    header_info_area_text = clean_text(header_info_area.text)
    header_info_list = [f.strip() for f in header_info_area_text.split('|')]

    var['uploader'] = header_info_list[0] + ' ' + header_info_list[1]
    var['contact'] = header_info_list[2]

    context_area = content_info_area.find('div', class_='bbs-view-content')
    var['post_text'] = clean_text(context_area.text)
    var['post_image_url'] = search_img_list_in_contents(context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result