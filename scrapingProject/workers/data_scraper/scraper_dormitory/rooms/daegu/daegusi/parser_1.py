from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-25 
    var['post_id_idx'] = 0
    var['table_header'] = ["번호", "공모·모집명", "담당부서", "등록일", "공모구분", "공모상태", "첨부", "공모결과", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'end_date'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_data_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for meta_data in tmp_meta_data_list:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        if '담당자' in meta_data_name:
            var['contact'] = meta_data_value
        elif '접수기간' in meta_data_name:
            var['start_date'], var['end_date'] = parse_date_text(meta_data_value)
    tbody = extract_children_tag(soup, 'tbody')
    tmp_contents_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for contents in tmp_contents_list:
        contents_name = extract_children_tag(contents, 'th', child_tag_attrs={'scope':'row'}, is_recursive=False)
        if not contents_name:
            var['post_text'] = extract_text(contents)
            if not var['contact']:
                var['contact'] = extract_contact_numbers_from_text(extract_text(contents)) 
            var['post_image_url'] = search_img_list_in_contents(contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result

def parse_date_text(text):
    text_split = text.split(' ~ ')
    if len(text_split) == 2 :
        text_split_convert_to_datetime_string = [convert_datetime_string_to_isoformat_datetime(_[:10]) for _ in text_split]
        return text_split_convert_to_datetime_string[0], text_split_convert_to_datetime_string[1]
    else :
        return None, None

