from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', "post_subject"]
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-12
    var['post_id_idx'] = 0
    table_header = ["번호", "분류", "제목", "작성일자"]
    result = parse_board_type_html_page(soup, var, key_list, table_header)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list= extract_children_tag(soup, 'th', is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '조회수' in th_text:
            var['view_count']= extract_numbers_in_text(
                extract_text(
                    find_next_tag(th)
                )
            )
        elif '작성자' in th_text:
            uploader = extract_text(find_next_tag(th))
            var['uploader'] = uploader
            var['contact'] = extract_contact_numbers_from_text(uploader)
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'bbs_contents'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

