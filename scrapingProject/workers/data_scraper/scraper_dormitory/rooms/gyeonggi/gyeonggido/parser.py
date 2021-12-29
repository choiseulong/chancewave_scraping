from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

POST_URL_FORMAT = '/bbs/boardView.do?bIdx={bIdx}&bsIdx={bsIdx}&bcIdx={bcIdx}&menuId=1590&isManager=false&isCharge=false&page=1'


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type': ['post_url', 'post_title', 'post_subject', 'uploaded_time', 'view_count']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    # 2021-12-28 json 항목 매핑
    # CATEGORY_NAME : 분류
    # SUBJECT : 제목
    # VIEW_CNT : 조회수
    # WRITE_DATE2 : 작성일
    # CATEGORY_NAME : 민간위탁·대행

    for tmp_obj in json_data['items']:
        tmp_post_url = POST_URL_FORMAT.format(bIdx=tmp_obj['B_IDX'], bsIdx=tmp_obj['BS_IDX'], bcIdx=tmp_obj['BC_IDX'])
        var['post_url'].append(var['channel_main_url'][:-1] + tmp_post_url)
        var['post_title'].append(tmp_obj['SUBJECT'])
        var['post_subject'].append(tmp_obj['CATEGORY_NAME'])
        var['view_count'].append(tmp_obj['VIEW_CNT'])
        var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(tmp_obj['WRITE_DATE2']))

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type': ['post_text', 'uploader'],
        'multiple_type': ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    content_area = extract_children_tag(soup, 'div', {'class': 's-v-board-default'},
                                        is_child_multiple=False)

    content_info_header_area = extract_children_tag(content_area, 'div', {'class': 'header'},
                                                    is_child_multiple=False)
    content_info_header_list = extract_children_tag(content_info_header_area, 'dl',
                                                    is_child_multiple=False)
    content_info_header_list = extract_children_tag(content_info_header_list, 'dd',
                                                    is_child_multiple=True)

    for tmp_info_header in content_info_header_list:
        tmp_column = tmp_info_header.strong
        tmp_column_value = tmp_column.nextSibling.text.strip()
        if tmp_column.text.strip() == '작성자':
            var['uploader'] = tmp_column_value

    content_post_area = extract_children_tag(content_area, 'div', {'class': 'content'})

    var['post_text'] = clean_text(extract_text(content_post_area))
    var['post_image_url'] = search_img_list_in_contents(content_post_area, var['channel_main_url'])

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result
