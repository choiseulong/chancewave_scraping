from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 : 
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 2 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    
    result = merge_var_to_dict(key_list, var)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    info = extract_children_tag(soup, 'div', {'class' : 'info'}, is_child_multiple=False)
    strongList = extract_children_tag(info, 'strong', child_tag_attrs={}, is_child_multiple=True)
    for strong in strongList:
        strongText = extract_text(strong)
        if '연락처' in strongText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_parent_tag(strong)
                )
            )
            break
    substan = extract_children_tag(soup, 'div', {'class' : 'substan'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(substan))
    var['post_image_url'] = search_img_list_in_contents(substan, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    # print(result)
    return result


