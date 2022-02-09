from enum import IntEnum
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-01-26
    table_data_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'div_newsNotice'})
    data_list = extract_children_tag(table_data_box, 'li', is_child_multiple=True)
    if data_list :
        data_list = data_list[1:]
    else :
        return
    for li in data_list :
        p_list = extract_children_tag(li, 'p', is_child_multiple=True)
        for p_idx, p_tag in enumerate(p_list):
            p_text = extract_text(p_tag)
            if p_idx == 0 and '공지' in p_text:
                if var['page_count'] != 1:
                    break
            if p_idx == 1:
                a_tag = extract_children_tag(p_tag, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(
                    extract_text(a_tag)
                )
            elif p_idx == 2:
                var['uploader'].append(p_text)
            elif p_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(p_text)
                )
            elif p_idx == 5:
                var['view_count'].append(
                    extract_numbers_in_text(p_text)
                )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    info_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'titles'}, is_child_multiple=True)
    for info in info_list:
        info_text = extract_text(info)
        if '전화번호' in info_text:
            var['contact'] = extract_contact_numbers_from_text(
                    extract_text(
                        find_next_tag(info)
                    )
                )
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'contents'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact'] :
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

