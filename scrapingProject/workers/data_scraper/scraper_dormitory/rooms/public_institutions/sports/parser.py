from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2022-01-13 
    var['post_id_idx'] = 0
    var['table_header'] = ["번호", "제목", "파일", "담당부서", "담당자", "등록일"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope' : 'row'}, is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '전화번호' in th_text:
            var['contact'] = extract_text(find_next_tag(th))
        elif '조회수' in th_text:
            var['view_count'] = extract_numbers_in_text(
                extract_text(find_next_tag(th))
            )
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'board_content'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

