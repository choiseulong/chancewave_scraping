from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-10
    var['table_header'] = ["번호", "제목", "등록일", "조회수", "첨부파일"]
    result = parse_board_type_html_page(soup, var, key_list)  
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'view_count', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_detail_info = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_detail_info'})
    var['post_title'] = extract_text_from_single_tag(board_detail_info, 'h2')

    info_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'info_b'})
    info_list = extract_children_tag(info_box, 'dt', is_child_multiple=True)
    for info in info_list:
        info_text = extract_text(info)
        info_value = extract_text(find_next_tag(info))
        if '전화' in info_text:
            var['contact'] = info_value
        elif '담당자' in info_text:
            var['uploader'] = info_value
        elif '조회' in info_text:
            var['view_count'] = extract_numbers_in_text(info_value)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_detail_contents'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

