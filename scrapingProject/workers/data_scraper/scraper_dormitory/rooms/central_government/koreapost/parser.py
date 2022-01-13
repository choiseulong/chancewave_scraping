from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'view_count', 'uploader', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 2:
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                post_url = extract_attrs(a_tag, 'href')
                if 'http' not in post_url:
                    post_url = var['channel_main_url'] + post_url
                var['post_url'].append(post_url)
                var['post_title'].append(td_text)
            elif td_idx == 3:
                var['uploader'].append(td_text)
            elif td_idx == 4:    
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5:
                var['view_count'].append(extract_numbers_in_text(td_text))

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
    contentsBox = extract_children_tag(soup, 'div', {'class' : 'seed_tbl'}, is_child_multiple=False)
    thList = extract_children_tag(contentsBox, 'th', {'scope' : 'row'}, is_child_multiple=True)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(find_next_tag(th))
            )
            break
    seedbbsContentWrap = extract_children_tag(contentsBox, 'div', {'class' : 'seedbbsContentWrap'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(seedbbsContentWrap))
    var['post_image_url'] = search_img_list_in_contents(seedbbsContentWrap, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result