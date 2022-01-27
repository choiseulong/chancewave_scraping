from pickle import FALSE
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_thumbnail', 'post_title', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_post_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'course_list'})
    post_list = extract_children_tag(tmp_post_box, 'li', is_child_multiple=True, is_recursive=False)
    if not post_list : 
        return
    for post in post_list :
        img = extract_children_tag(post, 'img')
        src = extract_attrs(img, 'src')
        var['post_thumbnail'].append(
            var['channel_main_url'] + src
        )
        tmp_meta_data_box = extract_children_tag(post, 'div', child_tag_attrs={'class':'list_sub'})
        var['post_title'].append(
            extract_text_from_single_tag(tmp_meta_data_box, 'p') \
            + ' - ' \
            + extract_text_from_single_tag(tmp_meta_data_box, 'strong')
        )
        btn_box = extract_children_tag(post, 'div', child_tag_attrs={'class':'btn_wrap'})
        btn_list = extract_children_tag(btn_box, 'a', is_child_multiple=True)
        for btn_idx, btn in enumerate(btn_list):
            if btn_idx == 0:
                btn_text = extract_text(btn)
                if btn_text == '교육종료':
                    var['is_going_on'].append(
                        False
                    )
                else:
                    print(btn_text, 'is_going_on 처리가 필요합니다.')
                    var['is_going_on'].append(
                        True
                    )
            elif btn_idx == 1:
                href = extract_attrs(btn, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'start_date', 'end_date', 'start_date2', 'end_date2'],
        'multiple_type' : ['post_image_url', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'course_notice0'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])

    tmp_meta_data_list_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'info_list'})
    meta_data_list = extract_children_tag(tmp_meta_data_list_box, 'li', is_child_multiple=True, is_recursive=FALSE)
    extra_info = {'info_title' : '강좌상세'}
    for meta_data in meta_data_list:
        meta_data_title = extract_text_from_single_tag(meta_data, 'strong')
        meta_data_value = extract_text(meta_data).replace(meta_data_title, '')
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_title, meta_data_value)})
        if '접수기간' in meta_data_title:
            var['start_date'], var['end_date'] = parse_date_text(meta_data_value)
        elif '교육기간' in meta_data_title:
            if '~' in meta_data_value :
                meta_data_value_split = meta_data_value.split(' ~ ')
                var['start_date2'] = convert_datetime_string_to_isoformat_datetime(meta_data_value_split[0])
                var['end_date2'] = convert_datetime_string_to_isoformat_datetime(meta_data_value_split[1])
            else :
                var['start_date2'] = None
                var['end_date2'] = None
        elif '문의전화' in meta_data_title:
            if meta_data_value:
                var['contact'] = meta_data_value
    var['extra_info'] = extra_info
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    convert_datetime_string_to_isoformat_datetime
    text_split = \
    [
        convert_datetime_string_to_isoformat_datetime(i[:10]) \
        for i \
        in text.split(' ~ ')
    ] if '~' \
    in text \
    else [None, None]
    return text_split[0], text_split[1]
