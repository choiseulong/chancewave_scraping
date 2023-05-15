from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-26
    var['post_id_idx'] = 0
    var['table_header'] = ["번호", "제목", "작성자", "조회수", "등록일", "첨부파일"]
    result = parse_board_type_html_page(soup, var, key_list)
    print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'bbs--view--cont'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['post_text']:
        iframe = extract_children_tag(soup, 'iframe', child_tag_attrs={'id':'pdf'})
        if iframe :
            src = extract_attrs(iframe, 'src')
            var['post_text'] = var['channel_main_url'] + src
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    print(result)

    return result

