from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    if not tr_list:
        return
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        uploader = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text:
                if var['page_count'] == 1 :
                    pass
                else :
                    break
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', child_tag_attrs={}, is_child_multiple=False)
                onclick = extract_attrs(a_tag, 'onclick')
                postId = parse_post_id(onclick, 4)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
                var['post_title'].append(td_text)
            elif td_idx in [3, 4]:
                uploader += td_text + ' '
            elif td_idx == 6:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 5:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
        if '공지' not in td_text:
            var['uploader'].append(uploader)
    
    result = merge_var_to_dict(key_list, var)
    
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view_info = extract_children_tag(soup, 'div', {'class' : 'view_info'}, is_child_multiple=False)
    liList = extract_children_tag(view_info, 'li', child_tag_attrs={}, is_child_multiple=True)
    for li in liList:
        liText = extract_text(li)
        if '작성자' in liText:
            var['contact'] = extract_contact_numbers_from_text(liText)
            break
    view_cont = extract_children_tag(soup, 'div', {'class' : 'view_cont'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(view_cont))
    var['post_image_url'] = search_img_list_in_contents(view_cont, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    
    return result


