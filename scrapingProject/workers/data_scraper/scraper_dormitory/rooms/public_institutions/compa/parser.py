from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    form_list = extract_children_tag(tbody, 'form', is_child_multiple=True)
    if len(tr_list) != len(form_list): 
        return
    # 22-01-12 header ['번호', '제목', '작성자', '작성일', '조회수']
    for tr_idx, tr in enumerate(tr_list):
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a')
                form = form_list[tr_idx]
                form_attrs_action = extract_attrs(form, 'action')
                post_url = var['channel_main_url'] + form_attrs_action + '?'
                form_input_list = extract_children_tag(form, 'input', is_child_multiple=True)
                params_text = ''
                for input in form_input_list:
                    input_attrs_name = extract_attrs(input, 'name')
                    input_attrs_value = extract_attrs(input, 'value')
                    p = input_attrs_name + '=' + input_attrs_value
                    params_text += p + '&'
                post_url = post_url + params_text
                var['post_url'].append(post_url)
            elif td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 4 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_subject'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    li_list = extract_children_tag(soup, 'li', is_child_multiple=True)
    for li in li_list:
        li_text = extract_text(li)
        if '카테고리' in li_text:
            var['post_subject'] = li_text.split(':')[1].strip()
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'viewContents'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

