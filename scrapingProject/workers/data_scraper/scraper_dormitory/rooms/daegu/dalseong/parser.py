from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'uploader', 'contents_req_params']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    if not tr_list :
        return
    # 2021-01-06 header [번호, 제목, 부서명, 등록일, 첨부, 조회]
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        td_text = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td).strip()
            if '공지' in td_text and td_idx == 0:
                if var['page_count'] != 1:
                    break
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                onclick = extract_attrs(a_tag, 'onclick')
                post_id = parse_post_id(onclick)
                var['contents_req_params'].append(
                    {
                        "menu_id" :"00000193",
                        "bbsId" : "BBS_00072",
                        "bbsTyCode" : "BBST03",
                        "bbsAttrbCode" : "BBSA03",
                        "nttId" : post_id
                    }
                )
            elif td_idx == 5:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        if '제목' in dt_text:
            var['post_title'] = extract_text(
                    find_next_tag(dt)
                )
        elif '작성자' in dt_text:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(dt)
                )
            )
    tmp_contents = extract_children_tag(soup, 'dl', child_tag_attrs={'class' : 'content'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

