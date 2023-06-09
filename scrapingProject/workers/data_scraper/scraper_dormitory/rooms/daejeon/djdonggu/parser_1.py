from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'contents_req_params', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    if not tr_list :
        return
    # 22-01-19 header ["번호", "제목", "작성자", "작성일", "첨부", "조회수"]
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        is_notice = False
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text and td_idx == 0:
                if var['page_count'] != 1 :
                    is_notice = True
                    break
            if td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
        if not is_notice:
            form = extract_children_tag(tr, 'form')
            input_list = extract_children_tag(form, 'input', is_child_multiple=True)
            req_params = {}
            for input in input_list:
                input_name = extract_attrs(input, 'name')
                input_value = extract_attrs(input, 'value')
                req_params.update({input_name : input_value})
            var['contents_req_params'].append(req_params)
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list = extract_children_tag(soup, 'th', is_child_multiple=True)
    for th in th_list :
        th_text = extract_text(th)
        if '제목' in th_text:
            var['post_title'] = extract_text(find_next_tag(th))
        elif '내용' in th_text:
            tmp_contents = find_next_tag(th)
            var['post_text'] = extract_text(tmp_contents)
            var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

