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
    # 2021-01-05 header [번호, 제목, 담당부서, 작성일, 첨부, 조회수]
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        td_text = ''
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td).strip()
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(td_text)
            elif td_idx == 2 :
                var['uploader'].append(td_text)
            elif td_idx == 5:
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
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    li_date = extract_children_tag(soup, 'li', child_tag_attrs={'class' : 'date'})
    if li_date :
        contact_text_split = extract_text(li_date).split(' : ')[1] if len(extract_text(li_date).split(' : ')) == 2 else ''
        var['contact'] = contact_text_split
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'bbs_detail_content'})
    var['post_text'] = extract_text(tmp_contents)
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    if not var['contact'] :
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents))
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

