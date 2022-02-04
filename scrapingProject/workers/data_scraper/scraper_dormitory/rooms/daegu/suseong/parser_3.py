from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploader', 'view_count', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-04
    var['post_id_idx'] = 1
    var['table_header'] = ["번호", "제목", "담당부서", "등록일", "첨부", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        dd_value =  extract_text(find_next_tag(dt))
        if '제목' in dt_text:
            var['post_title'] = dd_value
        elif '담당부서' in dt_text:
            var['contact'] = extract_contact_numbers_from_text(dd_value)
    tmp_contents = extract_children_tag(soup, 'dl', child_tag_attrs={'class':'content'})
    var['post_text'] = extract_text(tmp_contents).replace('글내용', '')
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

