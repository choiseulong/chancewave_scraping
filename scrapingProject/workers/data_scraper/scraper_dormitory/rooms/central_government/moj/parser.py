from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_subject', 'uploaded_time', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        tr_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for trIdx, tr in enumerate(tr_list):
            trText = extract_text(tr)
            if trIdx == 1:
                var['post_title'].append(trText)
                a_tag = extract_children_tag(tr, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(var['channel_main_url'] + href)
            elif trIdx == 2 : 
                var['post_subject'].append(trText)
            elif trIdx == 3 :
                var['uploader'].append(trText)
            elif trIdx == 5 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(trText)
                )
            elif trIdx == 6 :
                var['view_count'].append(
                    extract_numbers_in_text(trText)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dtList = extract_children_tag(soup, 'dt', child_tag_attrs={}, is_child_multiple=True)
    for dt in dtList:
        dtText = extract_text(dt)
        if '전화번호' in dtText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(dt)
                )
            )
            break
    artclView = extract_children_tag(soup, 'div', {'class' : 'artclView'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(artclView))
    var['post_image_url'] = search_img_list_in_contents(artclView, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result