from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'start_date', 'end_date']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-08
    var['table_header'] = ["글번호", "제목", "시작일", "종료일", "장소"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader', 'uploaded_time', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    meta_data_list = extract_children_tag(tbody, 'td', is_child_multiple=True)
    for meta_data_idx, meta_data in enumerate(meta_data_list) :
        meta_data_text = extract_text(meta_data)
        if meta_data_idx == 0 :
            var['uploader'] = meta_data_text
        elif meta_data_idx == 1 :
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(meta_data_text[:-1])
        elif meta_data_idx == 2:
            var['view_count'] = extract_numbers_in_text(meta_data_text)
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    tmp_contents = tr_list[-1]
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
