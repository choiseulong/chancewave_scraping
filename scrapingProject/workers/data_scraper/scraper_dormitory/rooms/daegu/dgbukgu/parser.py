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
    # 2021-01-06 header [번호, 제목, 담당부서, 등록일, 첨부, 조회]
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        td_text = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td).strip()
            if not td_text and td_idx == 0 :
                if var['page_count'] != 1 :
                    break
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                onclick = extract_attrs(a_tag, 'onclick')
                post_id = parse_post_id(onclick)
                req_params = {
                    "menu_id" : "00000195",
                    "bbsId" : "BBSMSTR_000000001176",
                    "bbsTyCode" : "BBST01", 
                    "bbsAttrbCode" : "BBSA03",
                    "nttId" : post_id
                }
                var['contents_req_params'].append(req_params)
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
    th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope' : 'row'}, is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '제목' in th_text or 'Notice Subject' in th_text:
            next_tag = find_next_tag(th)
            decomposed_next_tag = decompose_tag(next_tag, 'span')
            var['post_title'] = extract_text(decomposed_next_tag)
        elif '담당부서' in th_text:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(th)
                )
            )
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'bbsViewBody'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

