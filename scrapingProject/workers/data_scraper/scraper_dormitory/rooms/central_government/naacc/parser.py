from typing_extensions import Literal
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board'})
    tr_list = extract_children_tag(cont_box, 'tr', is_child_multiple=True)
    for tr in tr_list:
        a_tag = extract_children_tag(tr, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, 0)
        var['post_url'].append(
            var['post_url_frame'].format(post_id)
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        info_list = extract_children_tag(tr, 'li', is_child_multiple=True)
        for info_idx, info in enumerate(info_list):
            info_text = extract_text(info)
            if info_idx == 0:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(info_text)
                )
            elif info_idx == 1:
                var['uploader'].append(info_text)
            elif info_idx == 2:
                var['view_count'].append(extract_numbers_in_text(info_text))
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    con = extract_children_tag(soup, 'div', {'class' : 'boardDetailContents'})
    post_text = extract_text(con)
    var['post_text'] = clean_text(post_text)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(con, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
