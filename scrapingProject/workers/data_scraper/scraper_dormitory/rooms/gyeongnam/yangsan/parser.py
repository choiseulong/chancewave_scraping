from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text:
                if var['page_count'] == 1 :
                    pass
                else :
                    continue
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
                onclick = extract_attrs(a_tag, 'onclick')
                postId = parse_onclick(onclick)
                var['post_url'].append(
                    var['post_url_frame'].format(postId)
                )
                var['uploader'].append(
                    extract_text(
                        extract_children_tag(td, 'span', {'class' : 'list_dept'}, DataStatus.not_multiple)
                    )
                )
            elif td_idx == 3 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 4 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view_info = extract_children_tag(soup, 'div', {'class' : 'view_info'}, DataStatus.not_multiple)
    tit = extract_children_tag(view_info, 'div', {'class' : 'tit'}, DataStatus.not_multiple)
    var['post_title'] = extract_text(tit)
    view_cont = extract_children_tag(soup, 'div', {'class' : 'view_cont'}, DataStatus.not_multiple)
    post_text = extract_text(view_cont)
    var['post_text'] = clean_text(post_text)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(view_cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    print(result)
    return result
