from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

POST_URL_FORMAT = '/bbs/boardView.do?bIdx={bIdx}&bsIdx={bsIdx}&bcIdx={bcIdx}&menuId=1590&isManager=false&isCharge=false&page=1'


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    # 2021-12-31 HYUN
    # html table header index
    table_column_list = ['번호', '제목', '첨부', '담당부서', '작성일', '조회']

    # 게시물 리스트 테이블 영역
    post_list_table_bs = soup.find('div', class_='board_wrap_bbs').find('table')

    # 테이블 컬럼 영역
    post_list_table_header_area_bs = post_list_table_bs.find('thead')
    # 테이블 칼럼 리스트
    post_list_table_header_list_bs = post_list_table_header_area_bs.find_all('th')

    post_row_list = post_list_table_bs.find('tbody').find_all('tr')

    for tmp_post_row in post_row_list:

        for idx, tmp_td in enumerate(tmp_post_row.find_all('td')):
            if idx == 0:
                if tmp_td.text.strip() == '공지':
                    # 번호에 공지가 있는 경우 리스트에 중복 출현하므로 처리 X
                    break
            elif idx == 1:
                var['post_title'].append(tmp_td.text.strip())
                var['post_url'].append(var['channel_main_url'] + tmp_td.find('a').get('href'))
            elif idx == 3:
                var['uploader'].append(tmp_td.text.strip())
            elif idx == 4:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_td.text.strip()))
            elif idx == 5:
                var['view_count'].append(extract_numbers_in_text(tmp_td.text.strip()))

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'uploader'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_info_area = soup.find('div', class_='board_wrap_bbs').find('table')

    content_info_header_area = content_info_area.find('thead')
    content_info_header_row_list = content_info_header_area.find_all('tr')

    for tmp_header_row in content_info_header_row_list:
        tmp_header_row.

        tmp_column_title = tmp_info_header.get('th').text.strip()
        tmp_column_value = tmp_info_header.get('tdnextSibling.text.strip()
        if tmp_column.text.strip() == '작성자':
            var['uploader'] = tmp_column_value

    content_post_area = extract_children_tag(content_area, 'div', {'class': 'content'})

    var['post_text'] = clean_text(extract_text(content_post_area))
    var['post_image_url'] = search_img_list_in_contents(content_post_area, var['channel_main_url'])

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    print(result)
    return result
