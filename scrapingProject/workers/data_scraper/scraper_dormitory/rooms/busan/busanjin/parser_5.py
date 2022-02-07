from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'is_going_on', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_cont_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'gallery01'})
    if type(tmp_cont_box) == type(None):
        return
    cont_list = extract_children_tag(tmp_cont_box, 'li', is_child_multiple=True, is_recursive=False)
    for cont in cont_list:
        a_tag = extract_children_tag(cont, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, 0)
        var['post_url'].append(
            var['post_url_frame'].format(post_id)
        )
        var['post_title'].append(
            extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'course-tit'})
        )
        is_going_on = extract_text_from_single_tag(cont, 'i', child_tag_attrs={'class':'Accept'})
        if '마감' in is_going_on:
            var['is_going_on'].append(False)
        else :
            print(var['channel_code'], 'is_going_on 체크')
            var['is_going_on'].append(True)
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'start_date2', 'end_date', 'end_date2', 'uploader'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_meta_info_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'edu-dt-listtype01'})
    meta_info_list = extract_children_tag(tmp_meta_info_box, 'li', is_child_multiple=True)
    extra_info = {'info_title':'교육상세'}
    for meta_info in meta_info_list:
        info_name = extract_text_from_single_tag(meta_info, 'span', child_tag_attrs={'class':'tit'})
        info_value = extract_text(meta_info).replace(info_name, '').strip()
        extra_info.update({f'info_{len(extra_info)}': (info_name, info_value)})
        if '주최' in info_name:
            var['uploader'] = info_value
        elif '강좌기간' in info_name:
            var['start_date2'], var['end_date2'] = parse_date_text(info_value)
        elif '접수기간' in info_name:
            var['start_date'], var['end_date'] = parse_date_text(info_value)
    var['extra_info'].append(
        extra_info
    )    
    tmp_contents = extract_children_tag(soup, 'p', child_tag_attrs={'class':'con-txt'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.split(' ~ ')
    if len(text_split) == 2:
        result = [convert_datetime_string_to_isoformat_datetime(_[:10]) for _ in text_split]
        return result[0], result[1]
    else:
        return None, None