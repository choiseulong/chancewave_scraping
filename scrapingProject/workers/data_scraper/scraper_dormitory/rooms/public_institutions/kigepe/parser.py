from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 22-01-13
    table_header = ["No", "제목", "담당부서", "등록일", "첨부", "조회"]
    result = parse_board_type_html_page(soup, var, key_list, table_header)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '전화번호' in th_text:
            var['contact'] = extract_text(find_next_tag(th))
            break
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'subContent'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

