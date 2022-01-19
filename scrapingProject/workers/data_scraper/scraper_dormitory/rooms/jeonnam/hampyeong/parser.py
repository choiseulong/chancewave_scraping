from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_list_body = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'body_row'}, is_child_multiple=True)
    for div in board_list_body :
        sub_div_list = extract_children_tag(div, 'div', is_child_multiple=True)
        div_text = ''
        # 2021-12-31 header [번호, 제목, 작성자, 작성일, 파일, 조회]
        for div_idx, sub_div in enumerate(sub_div_list):
            div_text = extract_text(sub_div)
            if div_idx == 1:
                a_tag = extract_children_tag(sub_div, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(div_text)
            elif div_idx == 2 :
                var['uploader'].append(div_text)
            elif div_idx == 5:
                var['view_count'].append(
                    extract_numbers_in_text(div_text)
                )
            elif div_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(div_text)
                )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_view_info = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_view_info'})
    var['contact'] = extract_contact_numbers_from_text(extract_text(board_view_info))
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_view_body'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


