from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        uploader = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx in [2] :
                uploader += td_text + ' '
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
        var['uploader'].append(uploader)
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    bbs_view2 = extract_children_tag(soup, 'div', {'class' : 'bbs_view2'}, DataStatus.not_multiple)
    strongList = extract_children_tag(bbs_view2, 'strong', DataStatus.empty_attrs, DataStatus.multiple)
    for strong in strongList:
        strongText = extract_text(strong)
        if '전화번호' in strongText:
            parent = find_parent_tag(strong)
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(parent)
            )
            break

    bbs_con = extract_children_tag(bbs_view2, 'div', {'class' : 'bbs_con'}, DataStatus.not_multiple)
    var['post_text'] = extract_text(bbs_con)
    var['post_image_url'] = search_img_list_in_contents(bbs_con, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result


