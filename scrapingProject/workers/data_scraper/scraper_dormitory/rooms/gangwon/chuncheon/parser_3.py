from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-02-09 
    var['table_header'] = ["글번호", "제목", "작성자", "작성일"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_title'] = extract_text_from_single_tag(soup, 'div', child_tag_attrs={'class':'board-tit'})
    tit_list = extract_children_tag(soup, 'span', child_tag_attrs={'class':'tit'}, is_child_multiple=True)
    for tit in tit_list:
        tit_text = extract_text(tit)
        if '조회수' in tit_text:
            var['view_count'] = extract_numbers_in_text(
                extract_text(
                    find_next_tag(tit)
                )
            )
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board-con'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

