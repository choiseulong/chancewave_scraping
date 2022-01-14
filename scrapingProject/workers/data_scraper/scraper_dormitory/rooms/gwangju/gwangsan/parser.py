from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-14 
    var['table_header'] = ["번호", "제목", "작성자", "작성일", "조회"]
    result = parse_board_type_html_page(soup, var, key_list)
    print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_viewInfo = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'board_viewInfo'})
    li_list = extract_children_tag(board_viewInfo, 'li', is_child_multiple=True)
    for li in li_list:
        li_text = extract_text(li)
        if '문의전화' in li_text:
            var['contact'] = extract_contact_numbers_from_text(li_text)
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board_viewInfo'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class':'mt50'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    print(result)

    return result

