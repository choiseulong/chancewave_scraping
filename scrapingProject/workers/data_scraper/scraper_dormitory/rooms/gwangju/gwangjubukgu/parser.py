from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-17 
    dhead = extract_children_tag(soup, 'div', child_tag_attrs={'class':'dhead'})
    var['table_header_box'] = extract_children_tag(dhead, 'ul')
    var['table_data_box'] = extract_children_tag(soup, 'div', child_tag_attrs={'class':'dbody'})
    var['table_header'] = ["번호", "제목", "작성부서", "작성일자", "첨부", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'tb_contents'})
    sub_div = extract_children_tag(tmp_contents, 'div', is_child_multiple=True)
    if sub_div:
        sub_div_count = len(sub_div)
        for _ in range(sub_div_count): 
            tmp_contents = decompose_tag(tmp_contents, 'div')
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

