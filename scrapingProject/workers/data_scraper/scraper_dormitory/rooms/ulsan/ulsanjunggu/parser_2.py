from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-24 
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
    uploader = ''
    for li in li_list:
        li_text = extract_text(li)
        if '부서명' in li_text:
            uploader += li_text.replace('부서명', '').strip()
        elif '작성자' in li_text:
            uploader += li_text.replace('부서명', '').strip()
    var['uploader'] = uploader
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'b_con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

