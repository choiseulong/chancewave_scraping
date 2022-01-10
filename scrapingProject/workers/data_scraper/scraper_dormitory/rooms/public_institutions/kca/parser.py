from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_subject', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-01-10 header ["번호", "분류", "제목", "작성자", "작성일", "파일", "조회"]
    post_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'listBody-row'}, is_child_multiple=True)
    # 2021-01-10 header ["번호", "분류", "제목", "작성자", "작성일", "파일", "조회"]
    for post in post_list:
        p_list = extract_children_tag(post, 'p', is_child_multiple=True)
        for p_idx, p in enumerate(p_list):
            p_text = p.text
            if p_idx == 1 :
                var['post_subject'].append(
                    p_text
                )
            elif p_idx == 2 :
                a_tag = extract_children_tag(p, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(p_text)
            elif p_idx == 3:
                var['uploader'].append(p_text)
            elif p_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(p_text)
                )
            elif p_idx == 6:
                var['view_count'].append(
                    extract_numbers_in_text(p_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'boardContents'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

