from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'view_count', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-08
    var['table_header'] = ['번호', '제목', '파일', '조회수', '작성일']
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_info = extract_children_tag(soup, 'th', is_child_multiple=True, child_tag_attrs={'scope':'row'})
    for meta_info in tmp_meta_info:
        meta_info_name = extract_text(meta_info)
        if '내용' in meta_info_name:
            tmp_contents = find_next_tag(meta_info)
            var['post_text'] = extract_text(tmp_contents)
            if not var['contact']:
                var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
