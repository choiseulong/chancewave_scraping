from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text:
                if var['page_count'] == 1 :
                    pass
                else :
                    continue

            if td_idx == 1 : 
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['post_url_frame'] + href
                )
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont = extract_children_tag(soup, 'td', {'class' : 'cont'}, DataStatus.not_multiple)
    post_text = extract_text(cont)
    var['post_text'] = clean_text(post_text)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result


