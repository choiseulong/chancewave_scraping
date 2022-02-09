from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_subject', 'post_url', 'post_title', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'class':'eduList2'})
    if type(None) == type(cont_box):
        return
    cont_list = extract_children_tag(cont_box, 'a', is_child_multiple=True)
    for cont in cont_list:
        href = extract_attrs(cont, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        title = extract_children_tag(cont, 'div', child_tag_attrs={'class':'eduTitle'})
        subject = extract_children_tag(title, 'span')
        post_subject = extract_text(subject)
        var['post_subject'].append(post_subject.replace('[','').replace(']',''))
        var['post_title'].append(
            extract_text(title).replace(post_subject, '')
        )
        p_list = extract_children_tag(cont, 'p', is_child_multiple=True)
        for p_tag in p_list :
            p_text = extract_text(p_tag)
            if '접수상태' in p_text:
                if '신청중' in p_text:
                    var['is_going_on'].append(True)
                elif '신청마감' in p_text:
                    var['is_going_on'].append(False)
                else :
                    var['is_going_on'].append('ERROR')
                break
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_text_type', 'start_date', 'end_date'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'
    info_box = extract_children_tag(soup, 'tbody')
    tmp_meta_date = extract_children_tag(info_box, 'th', is_child_multiple=True)
    extra_info = {'info_title':'강좌상세'}
    for meta_data in tmp_meta_date:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_name, meta_data_value)})
        if '연락처' in meta_data_name:
            var['contact'] = meta_data_value
        elif '교육기간' in meta_data_name:
            var['start_date'], var['end_date'] = parse_date_text(meta_data_value)
        elif '내용' in meta_data_name:
            tmp_contents = find_next_tag(meta_data)
            var['post_text'] = extract_text(tmp_contents)
            if not var['contact']:
                var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.split(' ~ ')
    if len(text_split) == 2:
        result = [convert_datetime_string_to_isoformat_datetime(_) for _ in text_split]
        return result[0], result[1]
    else :
        return None, None

