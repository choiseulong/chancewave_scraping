from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'post_url', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', {}, is_child_multiple=False)
    trList_all = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    if not trList_all: 
        return
    trList_info = extract_children_tag(tbody, 'tr', {'class' : 'info'}, is_child_multiple=True)
    validTrList = list(set(trList_all) - set(trList_info))
    for tr in validTrList :
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                var['post_url'].append(
                    var['channel_main_url'] + \
                    extract_attrs(
                        extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False), 'href'
                    )
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx == 3:
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        td_text
                    )
                )
            elif td_idx == 5 :
                var['view_count'].append(extract_numbers_in_text(td_text))

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    viewContent = extract_children_tag(soup, 'div', {'class':'view-contents'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(viewContent))
    var['post_image_url'] = search_img_list_in_contents(viewContent, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
