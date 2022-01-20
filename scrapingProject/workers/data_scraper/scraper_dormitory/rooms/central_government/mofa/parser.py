from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                onclick = extract_attrs(a_tag, 'onclick')
                post_id = parse_post_id(onclick, 0)
                var['post_url'].append(
                    var['post_url_frame'].format(post_id) 
                )
                var['post_title'].append(td_text)
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        if '조회' in dt_text:
            var['view_count'] = extract_numbers_in_text(
                extract_text(
                    find_next_tag(dt)
                )
            )
            break
    contentsBox = extract_children_tag(soup, 'div', {'class' : 'bo_con'})
    var['post_image_url'] = search_img_list_in_contents(contentsBox, var['channel_main_url'])
    var['post_text'] = extract_text(contentsBox)
    var['contact'] = extract_contact_numbers_from_text(extract_text(contentsBox))
    
    result = convert_merged_list_to_dict(key_list, var)
    return result