from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'view_count', 'post_url', 'post_subject', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont_box = extract_children_tag(soup, 'tbody')
    cont_list = extract_children_tag(cont_box, 'tr', is_child_multiple=True)
    for cont in cont_list :
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                var['post_subject'].append(td_text)
            elif td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                a_tag = extract_children_tag(cont, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 6:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 7:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
    result = merge_var_to_dict(key_list, var)
    # 2021-01-12
    # var['table_header'] = ["번호", "구분", "부서", "제목", "첨부파일", "작성자", "작성일", "조회수"]
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    var['post_title'] = extract_text_from_single_tag(tbody, 'strong')
    tmp_contents = extract_children_tag(soup, 'td', child_tag_attrs={'class' : 'conTd'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

