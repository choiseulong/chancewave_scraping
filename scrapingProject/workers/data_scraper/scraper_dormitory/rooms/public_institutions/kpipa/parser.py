from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-11
    table_header = ["번호", "분야", "제목", "등록일", "조회수"]
    result = parse_board_type_html_page(soup, var, key_list, table_header)
    print(result)
    return result

def parse_post_url(**params):
    td = params['td']
    var = params['var']
    a_tag = extract_children_tag(td, 'a')
    onclick = extract_attrs(a_tag, 'onclick')
    post_id_list = parse_post_id(onclick, [0,1])
    result = var['post_url_frame'].format(post_id_list[0], post_id_list[1])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '게시자' in th_text:
            var['uploader'] = extract_text(find_next_tag(th))
        elif '문의처' in th_text:
            var['contact'] = extract_text(find_next_tag(th))
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'bd01tdC'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

