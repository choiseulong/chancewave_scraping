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
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                postId = parse_post_id(extract_attrs(a_tag, 'onclick'), 0)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
                var['post_title'].append(td_text)
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

    
    result = merge_var_to_dict(key_list, var)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'start_date', 'end_date', 'start_date2', 'end_date2'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    thList = extract_children_tag(tbody, 'th', child_tag_attrs={}, is_child_multiple=True)
    dateCount = 0
    dateInfo = {'start_date' : '공지시작일', 'end_date' : '공지종료일', 'start_date2' : '게시시작일시', 'end_date2' : '게시종료일시'}
    for th in thList:
        thText = extract_text(th)
        for key in dateInfo:
            if dateInfo[key] in thText:
                dateString = extract_text(find_next_tag(th))
                if dateString:
                    var[key] = convert_datetime_string_to_isoformat_datetime(dateString)
                dateCount += 1
        if dateCount == 4:
            break
    board_contents = extract_children_tag(tbody, 'div', {'class' : 'board-contents'}, is_child_multiple=False)
    post_text = extract_text(board_contents)
    var['post_text'] = clean_text(post_text)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(board_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    # print(result)
    return result