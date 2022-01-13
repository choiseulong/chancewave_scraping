from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'text_center'}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', {'class' : False}, is_child_multiple=True)
    if not tr_list :
        return
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 :
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                if not a_tag :
                    break
                href = extract_attrs(a_tag, 'href')
                postId = extract_text_between_prefix_and_suffix('gsgeul_no=', '&pageIndex', href)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
            elif td_idx == 2 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        td_text
                    )
                )
            elif td_idx == 3 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'post_title', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', {'class' : 'notice_view'}, is_child_multiple=False)
    thList = extract_children_tag(table, 'th', child_tag_attrs={}, is_child_multiple=True)
    for th in thList:
        thText = extract_text(th)
        if '제목' in thText:
            var['post_title'] = extract_text(find_next_tag(th))
        elif '작성자' in thText:
            thText = extract_text(find_next_tag(th))
            var['uploader'] = thText
            var['contact'] = extract_contact_numbers_from_text(thText)
        if var['post_title'] and var['uploader']:
            break
        
    con_text = extract_children_tag(table, 'td', {'class' : 'con_text'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(con_text))
    var['post_image_url'] = search_img_list_in_contents(con_text, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result


