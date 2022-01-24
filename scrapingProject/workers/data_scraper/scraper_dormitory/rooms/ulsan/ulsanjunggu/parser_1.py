from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-22 
    var['table_header'] = ["번호", "제목", "등록일", "첨부", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_info = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'view_info'})
    li_list = extract_children_tag(tmp_info, 'li', is_child_multiple=True)
    for li in li_list:
        li_text = extract_text(li)
        if '전화번호' in li_text:
            var['contact'] = extract_contact_numbers_from_text(li_text)
        elif '기관명' in li_text:
            var['uploader'] = li_text.replace('기관명', '').strip()
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'b_con'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

