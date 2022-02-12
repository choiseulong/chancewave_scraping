from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'start_date', 'start_date2', 'end_date', 'end_date2']
    }

    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    info_root = {
        'post_title' : '$..lecNm', 'start_date' : '$..rstart', 'end_date' : '$..rend', 
        'start_date2':'$..lstart', 'end_date2':'$..lend', 'post_url':'$..lecId'
    }
    for key_name in info_root:
        data = search_value_in_json_data_using_path(json_data, info_root[key_name])
        for value in data:
            if 'date' in key_name and len(value) > 10:
                value = convert_datetime_string_to_isoformat_datetime(value.replace('.0', ''))
            if key_name == 'post_url' :
                value = var['post_url_frame'].format(value)
            var[key_name].append(
                value
            )
    result = merge_var_to_dict(key_list, var)
    return result

def parse_date_text(text):
    cutted_text = text.split(':')[1]
    text_split = cutted_text.split(' ~ ')
    if len(text_split) == 2:
        result = [convert_datetime_string_to_isoformat_datetime(_.strip()) for _ in text_split]
        return result[0], result[1]
    else :
        return None, None

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_content_target'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_info = extract_children_tag(soup, 'div', child_tag_attrs={'class':'list_info'})
    info_list = extract_children_tag(tmp_info, 'li', is_child_multiple=True)
    extra_info = {'info_title' : '강좌/교육 정보'}
    for info in info_list:
        info_name = extract_text_from_single_tag(info, 'b').strip()
        info_value = extract_text(info).replace(info_name, '').strip()
        extra_info.update({f'info_{len(extra_info)}' : (info_name, info_value)})
        if '대상' in info_name:
            var['post_content_target'] = info_value
        elif '문의전화' in info_name:
            var['contact'] = info_value
    var['extra_info'].append(extra_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'id':'detail-tab01'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

