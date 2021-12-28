from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'text_center'}, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', {'class' : False}, DataStatus.multiple)
    if not tr_list :
        return
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 :
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
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
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'post_title', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', {'class' : 'notice_view'}, DataStatus.not_multiple)
    thList = extract_children_tag(table, 'th', DataStatus.empty_attrs, DataStatus.multiple)
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
        
    con_text = extract_children_tag(table, 'td', {'class' : 'con_text'}, DataStatus.not_multiple)
    var['post_text'] = clean_text(extract_text(con_text))
    var['post_image_url'] = search_img_list_in_contents(con_text, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result


