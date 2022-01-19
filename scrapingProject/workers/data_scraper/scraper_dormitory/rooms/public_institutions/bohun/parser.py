from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-01-10 header ["번호", "제목", "파일", "작성자", "작성일", "조회"]
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    if not tr_list :
        return
    for tr in tr_list :
        td_list = [
            td \
            for td \
            in extract_children_tag(tr, 'td', is_child_multiple=True)\
            if extract_attrs(td, 'width') != "1"
        ]
        td_text = [extract_text(td).strip() for td in td_list]
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['post_url_frame'] + href
                )
            elif td_idx == 3:
                var['uploader'].append(td_text)
            elif td_idx == 4 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    th_list = extract_children_tag(tbody, 'th', is_child_multiple=True)
    for th in th_list:
        th_text = extract_text(th)
        if '제목' in th_text:
            var['post_title'] = extract_text(find_next_tag(th))
            break
    tmp_contents = extract_children_tag(tbody, 'table')
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

