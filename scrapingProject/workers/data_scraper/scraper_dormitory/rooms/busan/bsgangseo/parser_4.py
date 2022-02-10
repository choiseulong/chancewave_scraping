from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_cont_box = extract_children_tag(soup, 'tbody', is_child_multiple=True)
    if type(tmp_cont_box) == type(None):
        print(var['channel_code'], 'cont_box ERROR')
        return
    else:
        tmp_cont_box = tmp_cont_box[1]
    cont_list = extract_children_tag(tmp_cont_box, 'tr', is_child_multiple=True)
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            if td_idx == 1 :
                a_tag = extract_children_tag(cont, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(
                    extract_text_from_single_tag(cont, 'span', child_tag_attrs={'class':'ptit'})
                )
            elif td_idx == 6 :
                td_text = extract_text(td)
                if '마감' in td_text:
                    var['is_going_on'].append(
                        False
                    )
                else :
                    print(var['channel_url'], 'is_going_on check')
                    var['is_going_on'].append(
                        True
                    )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'start_date', 'start_date2', 'end_date', 'post_content_target', 'end_date2'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tmp_meta_info = extract_children_tag(tbody, 'th', is_child_multiple=True)
    extra_info = {'info_title':'강좌상세'}
    for meta_info in tmp_meta_info:
        meta_info_name = extract_text(meta_info)
        meta_info_value = extract_text(find_next_tag(meta_info)).strip()
        extra_info.update({f'info_{len(extra_info)}' : (meta_info_name, meta_info_value)})
        if '문의전화' in meta_info_name:
            var['contact'] = meta_info_value
        elif '신청기간' in meta_info_name:
            var['start_date'], var['end_date'] = parse_date_text(meta_info_value)
        elif '교유기간' in meta_info_name:
            var['start_date2'], var['end_date2'] = parse_date_text(meta_info_value)
        elif '교육대상' in meta_info_name:
            var['post_content_target'] = meta_info_value
    var['extra_info'].append(extra_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'p-lec-info'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.split(' ~ ')
    if len(text_split) == 2 :
        result = [convert_datetime_string_to_isoformat_datetime(_[:10]) for _ in text_split]
        return result[0], result[1]
    else :
        return None, None
