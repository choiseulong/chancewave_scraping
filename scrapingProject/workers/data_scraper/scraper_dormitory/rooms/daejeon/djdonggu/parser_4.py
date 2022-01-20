from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-01-20
    notice_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'notice_list'})
    li_list = extract_children_tag(notice_list, 'li', is_child_multiple=True)
    if li_list :
        li_list = li_list[1:]
    else :
        return
    
    for li in li_list:
        p_list = extract_children_tag(li, 'p', is_child_multiple=True)
        for p_idx, p_tag in enumerate(p_list):
            p_text = extract_text(p_tag)
            if '공지' in p_text and p_idx == 0 :
                if var['page_count'] != 1 :
                    break
            
            if p_idx == 1 :
                a_tag = extract_children_tag(p_tag, 'a')
                onclick = extract_attrs(a_tag, 'onclick')
                post_id = parse_post_id(onclick, 0)
                var['post_url'].append(
                    var['post_url_frame'].format(post_id)
                )
                var['post_title'].append(p_text)
            elif p_idx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(p_text)
                )
            elif p_idx == 3:
                var['uploader'].append(p_text)
            elif p_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(p_text)
                )

    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'contents'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

