from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-07
    # var['table_header'] = ["번호", "제목", "작성일", "조회"]
    var['table_header'] = ['번호', '제목', '파일', '크기', '작성일', '조회수']
    result = parse_board_type_html_page(soup, var, key_list)

    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_title'] = extract_text_from_single_tag(soup, 'tr', child_tag_attrs={'class':'subject'}).replace('제목 ', '')
    tmp_meta_info = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for meta_info in tmp_meta_info:
        info_name = extract_text(meta_info)
        if '작성자' in info_name:
            var['uploader'] = extract_text(find_next_tag(meta_info))
            break
    tmp_contents = extract_children_tag(soup, 'tr', child_tag_attrs={'class':'bbs_content_area'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
