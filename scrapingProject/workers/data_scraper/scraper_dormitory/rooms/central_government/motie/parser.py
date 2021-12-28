from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_subject', 'post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                var['post_subject'].append(td_text)
            elif td_idx == 2 :
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
                href = extract_attrs(a_tag, 'href')
                postId = extract_text_between_prefix_and_suffix('bbs_seq_n=', '&bbs_cd_n', href)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
            elif td_idx == 3:
                var['uploader'].append(td_text)
            elif td_idx == 4:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5:
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
    thList = extract_children_tag(soup, 'th', {'scope' : 'row'}, DataStatus.multiple)
    for th in thList :
        thText = extract_text(th)
        if '연락처' in thText:
            var['contact'] = extract_text(find_next_tag(th))
        elif '내용' in thText:
            nextTag = find_next_tag(th)
            var['post_text'] = clean_text(extract_text(nextTag))
            var['post_image_url'] = search_img_list_in_contents(nextTag, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result