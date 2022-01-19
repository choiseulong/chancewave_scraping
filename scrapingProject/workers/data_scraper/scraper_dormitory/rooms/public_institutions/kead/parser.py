from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', child_tag_attrs={'class' : 'listBoard_No1'})
    decomposed_table = decompose_tag(table, 'thead')
    tr_list = extract_children_tag(decomposed_table, 'tr', is_child_multiple=True)
    if not tr_list :
        return
    # 2021-01-10 header ["번호", "제목", "담당부서", "등록일", "첨부파일", "조회"]
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        td_text = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td).strip()
            if td_idx == 2:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 6:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 4:
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
    th_list = extract_children_tag(soup, 'th', is_child_multiple=True)
    uploader = ''
    for th in th_list:
        th_text = extract_text(th)
        th_next_text = extract_text(find_next_tag(th))
        if '제목' in th_text:
            var['post_title'] = th_next_text
        elif '담당부서' in th_text or '담당자' in th_text:
            uploader += th_next_text
        elif '내용' in th_text:
            tmp_contents = find_next_tag(th)
            var['post_text'] = extract_text(tmp_contents)
            var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
            var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    var['uplolader'] = uploader 
    
    result = convert_merged_list_to_dict(key_list, var)
    return result