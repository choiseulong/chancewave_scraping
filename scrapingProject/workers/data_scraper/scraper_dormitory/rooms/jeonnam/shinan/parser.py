from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url','uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    # 2021-12-30 header [번호, 제목, 등록자, 등록일, 조회] 
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'post_title', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # post_title
    tbody = extract_children_tag(soup, 'tbody')
    th_list = extract_children_tag(tbody, 'th', is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '제목' in th_text:
            var['post_title'] = extract_text(
                find_next_tag(th)
            )
            break
    # contact, uploader
    tmp_uploader_info = extract_children_tag(soup, 'div', child_tag_attrs={'class':'staff_info'})
    tmp_content = extract_children_tag(soup, 'td', {'class' : 'content'})
    uploader = ''
    if tmp_uploader_info:
        info_div_list = extract_children_tag(tmp_uploader_info, 'div', is_child_multiple=True)
        for div in info_div_list:
            div_text = extract_text(div)
            div_text_splited = div_text.split(' : ')[1] + ' '
            if '부서' in div_text or '담당자' in div_text:
                uploader += div_text_splited
            elif '연락처' in div_text:
                var['contact'] = div_text_splited
        tmp_content = decompose_tag(tmp_content, 'div', {'class':'staff_info'})
    else :
        var['contact'] = ''
    var['uploader'] = uploader
    
    # contact, post_text, post_image_url
    var['post_text'] = extract_text(tmp_content)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_content))
    var['post_image_url'] = search_img_list_in_contents(tmp_content, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result