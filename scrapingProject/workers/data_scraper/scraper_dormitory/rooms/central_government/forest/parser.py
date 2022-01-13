from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        uploader = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            # if td_idx == 0 and '공지' in td_text:
            #     break
            if td_idx == 1:
                strong = extract_children_tag(tr, 'strong', child_tag_attrs={}, is_child_multiple=False)
                uploader += extract_text(strong)[1:-1] + ' - '
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                href = extract_attrs(a_tag, 'href')
                postId = extract_text_between_prefix_and_suffix('nttId=', '&bbsId', href)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                ) 
                var['post_title'].append(
                    extract_attrs(a_tag, 'title')
                )
            elif td_idx == 2:
                uploader += td_text
                var['uploader'].append(uploader)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text[:10])
                )
            elif td_idx == 5:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    # print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'post_text_type'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    spanList = extract_children_tag(soup, 'span', {'class' : 'info_tit'}, is_child_multiple=True)
    for span in spanList:
        spanText = extract_text(span)
        if '작성자' in spanText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(span)
                )
            )
    contents = extract_children_tag(soup, 'div', {'class' : 'b_content'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(contents))
    var['post_image_url'] = search_img_list_in_contents(contents, var['channel_main_url'])
    dlList = extract_children_tag(soup, 'dl', child_tag_attrs={}, is_child_multiple=True)
    extra_info = {'info_title' : '행사 정보'}
    for dl in dlList:
        dlText = extract_text(dl)
        if '주소' in dlText or '위치' in dlText:
            extraInfoText = extract_text(find_next_tag(dl))
            if extraInfoText:
                lenExtraInfo = len(extra_info)
                extra_info.update({f'info_{lenExtraInfo}' : extraInfoText})
        if 'info_0' in extra_info.keys():
            var['extra_info'].append(extra_info)

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result