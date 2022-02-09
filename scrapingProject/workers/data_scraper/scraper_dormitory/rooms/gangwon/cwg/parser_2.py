from cv2 import merge
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    item_list = extract_children_tag(soup, 'li', is_child_multiple=True, child_tag_attrs={'class':'item'})
    if type(None) == type(item_list):
        return
    for item in item_list:
        a_tag = extract_children_tag(item, 'a')
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
        var['post_title'].append(
            extract_text_from_single_tag(item, 'div', child_tag_attrs={'class':'titlebox'})
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['uploaded_time', 'view_count'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'only_extra_info'
    info_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'infobox'})
    info_text_split = extract_text(info_box).split(' / ')
    for info in info_text_split:
        info_value = info.split(' : ')[1]
        if '작성일' in info:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(info_value.strip())
        elif '조회수' in info:
            var['view_count'] = extract_numbers_in_text(info_value)
    extra_info = {'info_title':'공연상세'}
    tmp_meta_data = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for meta_data in tmp_meta_data:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        extra_info.update({f'info_{len(extra_info)}':(meta_data_name, meta_data_value)})
    var['extra_info'].append(extra_info)   
    result = convert_merged_list_to_dict(key_list, var)
    return result

