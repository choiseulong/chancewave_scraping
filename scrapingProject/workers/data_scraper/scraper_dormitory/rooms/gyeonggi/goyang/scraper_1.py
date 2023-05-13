from workers.data_scraper.scraper_dormitory.scraping_default_usage import Scraper as ABCScraper
from workers.data_scraper.scraper_dormitory.scraper_tools.tools import *
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import js2py

# 채널 이름 : 고양

# 타겟 : 축제/행사
# 중단 시점 : 마지막 페이지 도달시

# HTTP Request
'''
    @post list
    
    method : GET
    url = http://www.goyang.go.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1007&q_currPage={page_count}
    header :
        None

'''
'''
    @post info
    method : GET
    url : http://www.goyang.go.kr/www/user/bbs/BD_selectBbs.do?q_bbsCode=1007&q_bbscttSn={post_id}&q_currPage=1&q_pClCode=
    header :
        None

'''
sleepSec = 1
isUpdate = True

js_fn_make_post_url_code = """
/** 상세폼으로 이동 */
function fnView(bbsCode, bbscttSn, cntxtCours, clCode, currPage, pClCode) {
    if (typeof pClCode == "undefined") {
        pClCode = "";
    }
    if (typeof clCode == "undefined") {
        clCode = "";
    }
    if (typeof currPage == "undefined") {
        currPage = "";
    }
    if (clCode == -1 || clCode == "" || clCode == null ||bbsCode == "1055" ||bbsCode == "1082" || bbsCode == "1083") {
        return cntxtCours+"/user/bbs/BD_selectBbs.do?q_bbsCode="+bbsCode+"&q_bbscttSn="+bbscttSn+"&q_currPage="+currPage+"&q_pClCode="+pClCode;
    } else {
        var url = cntxtCours+"/user/bbs/BD_selectBbs.do?q_bbsCode="+bbsCode+"&q_bbscttSn="+bbscttSn+"&q_clCode="+clCode+"&q_currPage="+currPage+"&q_pClCode="+pClCode;
        return cntxtCours+"/user/bbs/BD_selectBbs.do?q_bbsCode="+bbsCode+"&q_bbscttSn="+bbscttSn+"&q_clCode="+clCode+"&q_currPage="+currPage+"&q_pClCode="+pClCode;
    }
}
"""
js_fn_make_post_url = js2py.eval_js(js_fn_make_post_url_code)


class Scraper(ABCScraper):
    def __init__(self, session):
        super().__init__(session)
        self.channel_name = '고양시'
        self.post_board_name = '축제/행사'
        self.channel_main_url = 'http://www.goyang.go.kr'

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
        'multiple_type': ['post_url', 'post_title', 'uploader', 'view_count', 'uploaded_time']
    }

    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2022-2-3 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '작성자', '담당부서', '작성일', '파일', '조회수']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('table', class_='table-list')

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
            # 게시물이 없는 경우 & 페이지 끝
            if tmp_td.text.find('게시물이 없습니다.') > -1:
                print('PAGE END')
                return

            if idx == 1:
                var['post_title'].append(tmp_td.text.strip())
                tmp_post_url = None
                tmp_post_url = eval(tmp_td.find('a').get('onclick')[:-1].replace('fnView', 'js_fn_make_post_url'))
                if not tmp_post_url:
                    print(tmp_post_url)
                    raise ValueError('CAN NOT PARSE POST URL')
                var['post_url'].append(make_absolute_url(in_url=tmp_post_url.strip(), channel_main_url=var['response'].url))
            elif idx == 3:
                var['uploader'].append(tmp_td.text.strip())
            elif idx == 4:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(clean_text(tmp_td.text).strip()))
            elif idx == 6:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text))

    result = merge_var_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='bbs-article')

    content_info_header_area = content_info_area.find('ul', class_='article-info')
    content_context_area = content_info_area.find('div', class_='article-detail')

    var['post_text'] = clean_text(content_context_area.text)
    var['post_image_url'] = search_img_list_in_contents(content_context_area, var['response'].url)

    result = convert_merged_list_to_dict(key_list, var)
    if var['dev']:
        print(result)
    return result