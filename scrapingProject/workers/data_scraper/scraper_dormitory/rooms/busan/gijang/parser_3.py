from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploader', 'view_count', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-04 
    var['table_header'] = ["번호", "제목", "작성자", "첨부파일", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_data = extract_children_tag(soup, 'td', child_tag_attrs={'class':'rc'})
    tmp_meta_data_list = extract_children_tag(tmp_meta_data, 'span', is_child_multiple=True)
    for meta_data in tmp_meta_data_list:
        meta_data_name = extract_text(meta_data)
        if '작성일' in meta_data_name:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(
                meta_data_name.replace('작성일', '').strip()[:-1]
            )
            break
    tmp_contents = extract_children_tag(soup, 'tbody')
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact'] :
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
