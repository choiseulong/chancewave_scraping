from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-07
    var['post_id_idx'] = [1,2,3]
    var['table_header'] = ["번호", "제목", "파일", "담당부서", "작성자", "작성일", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bod_view = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bod_view'})
    var['post_title'] = extract_text_from_single_tag(bod_view, 'h4')
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'view_cont'})
    var['post_text'] = extract_text(tmp_contents).replace('/ufeff', '')
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
