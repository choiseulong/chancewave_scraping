from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-26
    var['table_header'] = ["번호", "제목", "작성일", "첨부", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact','uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    info_list = extract_children_tag(soup, 'th', is_child_multiple=True)
    for info in info_list:
        info_text = extract_text(info)
        if '전화번호' in info_text:
            var['contact'] = extract_text(
                    find_next_tag(info)
                )
        elif '작성자' in info_text:
            var['uploader'] = extract_text(
                find_next_tag(info)
            )
    tbody = extract_children_tag(soup, 'tbody')
    tmp_contents = extract_children_tag(tbody, 'tr', is_child_multiple=True)[-1]
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact'] :
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

