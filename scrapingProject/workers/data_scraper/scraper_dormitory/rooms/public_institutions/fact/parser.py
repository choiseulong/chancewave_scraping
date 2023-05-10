from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        if key != 'post_url':
            var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-10
    var['table_header'] = ["번호", "제목", "첨부파일", "작성자", "등록일", "조회수"]
    # var['table_header'] = ["번호", "제목", "첨부파일", "게시자", "등록일", "조회수"]

    tbody = extract_children_tag(soup, 'tbody', is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for tr in tr_list:
        onclick_attrs = extract_attrs(tr, 'onclick')
        post_number = extract_values_list_in_both_sides_bracket_text(onclick_attrs)[0]
        var['post_url'].append(var['post_url_frame'].format(post_number))

    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    main_td = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'main'})
    var['post_text'] = extract_text(main_td)
    var['contact'] = extract_contact_numbers_from_text(extract_text(main_td)) 
    var['post_image_url'] = search_img_list_in_contents(main_td, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result