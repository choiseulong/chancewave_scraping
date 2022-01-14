from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count', 'uploader', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    if not tr_list :
        return
    # 2021-01-05 header [번호, 제목, 담당부서, 작성일, 조회수, 파일]
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        td_text = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td).strip()
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['post_url_frame'] + href
                )
                var['post_title'].append(td_text)
            elif td_idx == 4:
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
        'single_type' : ['post_text', 'contact', 'start_date', 'end_date'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    th_list = extract_children_tag(soup, 'th', child_tag_attrs={'scope':'row'}, is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '시작일' in th_text:
            next_tag_text = extract_text(find_next_tag(th))
            if len(next_tag_text) != 10 :
                continue
            var['start_date'] = convert_datetime_string_to_isoformat_datetime(next_tag_text)
        elif '종료일' in th_text:
            next_tag_text = extract_text(find_next_tag(th))
            if len(next_tag_text) != 10 :
                continue
            var['end_date'] = convert_datetime_string_to_isoformat_datetime(next_tag_text)
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'bbs_content'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

