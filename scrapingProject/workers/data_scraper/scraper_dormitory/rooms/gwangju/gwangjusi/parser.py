from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 22-01-14 header = ["번호", "제목", "작성자", "작성일", "파일", "조회"]
    board_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'body_row'}, is_child_multiple=True)
    for post in board_list:
        subject = extract_children_tag(post, 'div', child_tag_attrs={'class':'subject'})
        a_tag = extract_children_tag(subject, 'a')
        var['post_title'].append(extract_text(subject))
        var['post_url'].append(
            var['channel_main_url'] + extract_attrs(a_tag ,'href')
        )
        var['uploader'].append(
            extract_text_from_single_tag(post, 'div', child_tag_attrs={'class':'writer'})
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(post, 'div', child_tag_attrs={'class':'date'})
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text_from_single_tag(post, 'div', child_tag_attrs={'class':'hit'})
            )
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'board_view_body'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class': 'koglSeView'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    print(result)
    return result

