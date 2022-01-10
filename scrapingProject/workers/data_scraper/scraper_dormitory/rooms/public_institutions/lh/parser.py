from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_subject', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-10
    table_header = ["번호", "지사", "분류", "제목", "게시일", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list, table_header)
    return result

def parse_post_url(**params):
    td = params['td']
    var = params['var']
    a_tag = extract_children_tag(td, 'a')
    onclick = extract_attrs(a_tag, 'onclick') if a_tag.has_attr('onclick') else ''
    post_id = parse_onclick(onclick)
    result = var['post_url_frame'].format(post_id)
    return result

def parse_onclick(onclick):
    return extract_values_list_in_both_sides_bracket_text(onclick)[0]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bbs_content'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    print(result)
    return result

