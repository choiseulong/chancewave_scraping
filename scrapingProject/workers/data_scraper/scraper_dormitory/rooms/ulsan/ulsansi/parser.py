from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    if not tr_list :
        return
    # 2021-01-05 header [번호, 제목, 첨부파일, 작성일자, 조회수]
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
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_title', 'uploader'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    th_list = extract_children_tag(tbody, 'th', child_tag_attrs={'scope' : 'row'}, is_child_multiple=True)
    uploader = ''
    for th in th_list :
        th_text = extract_text(th)
        next_tag = find_next_tag(th)
        next_text = extract_text(next_tag)
        if '담당부서' in th_text or '성명' in th_text:
            uploader += next_text + ' '
        elif '전화번호' in th_text:
            var['contact'] = next_text
        elif '제목' in th_text:
            var['post_title'] = next_text
        elif '내용' in th_text:
            var['post_text'] = next_text
            var['post_image_url'] = search_img_list_in_contents(next_tag, var['channel_main_url'])
    var['uploader'] = uploader
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    print(result)
    return result

