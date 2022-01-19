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
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        uploader = ''
        td_text = ''
        # 2021-12-29 header [번호, 제목, 담당부서, 등록일, 조회수]
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if '공지' in td_text and td_idx == 0:
                if var['page_count'] != 1 :
                    break
            if td_idx == 1 :
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href 
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx in [2] :
                uploader += td_text + ' '
            elif td_idx == 4:
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
        if '공지' not in td_text:
            var['uploader'].append(uploader)
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view_title_box = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'view_titlebox'})
    dt_list = extract_children_tag(view_title_box, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        if '연락처' in dt_text:
            var['contact'] = extract_text(
                find_next_tag(dt)
            )
            break
    cont = extract_children_tag(soup, 'div', {'class' : 'viewbox'})
    var['post_text'] = extract_text(cont)
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result


