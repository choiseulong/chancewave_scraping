from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    list_tit = extract_children_tag(soup, 'div', {'class' : 'list_tit'}, DataStatus.multiple)
    if not list_tit:
        return
    for div in list_tit :
        notice_check = extract_children_tag(div, 'i', {'class' : 'notice'}, DataStatus.not_multiple)
        if notice_check :
            if var['page_count'] != 1 :
                continue
        a_tag = extract_children_tag(div, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(
                extract_children_tag(div, 'strong', DataStatus.empty_attrs, DataStatus.not_multiple)
            )
        )
        em_list = extract_children_tag(div, 'em', DataStatus.empty_attrs, DataStatus.multiple)
        for em_idx, em in enumerate(em_list):
            em_text = extract_text(em)
            if em_idx == 0 :
                var['uploader'].append(em_text)
            elif em_idx == 1 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(em_text)
                )
            elif em_idx == 2:
                var['view_count'].append(
                    extract_numbers_in_text(em_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'post_title', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont = extract_children_tag(soup, 'div', {'class' : 'bbs_con'}, DataStatus.not_multiple)
    var['post_text'] = extract_text(cont)
    var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    print(result)
    return result


