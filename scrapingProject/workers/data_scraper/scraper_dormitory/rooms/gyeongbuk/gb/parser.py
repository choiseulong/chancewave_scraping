from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                postId = extract_text_between_prefix_and_suffix('&B_NUM=', '&B_STEP', href)
                B_STEP = extract_text_between_prefix_and_suffix('&B_STEP=', '&B_LEVEL', href)
                var['post_url'].append(
                    var['post_url_frame'].format(postId, B_STEP)
                )
                var['post_title'].append(td_text)
            elif td_idx == 3:
                var['uploader'].append(td_text)
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 5:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        '20' + td_text
                    )
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
    span_l = extract_children_tag(soup, 'span', {'class' : 'span_l'}, is_child_multiple=True)
    for span in span_l:
        spanText = extract_text(span)
        if '작성자' in spanText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(span)
                )
            )
            break
    content = extract_children_tag(soup, 'dl', {'class' : 'content'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(content))
    var['post_image_url'] = search_img_list_in_contents(content, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    # print(result)
    return result


