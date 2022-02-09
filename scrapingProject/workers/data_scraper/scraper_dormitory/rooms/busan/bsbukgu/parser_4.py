from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-02-07 header ["번호", "제목", "작성일", "조회수"]
    table_header_box = extract_children_tag(soup, 'tr', child_tag_attrs={'id':'boardbg'})
    cont_list_box = find_parent_tag(table_header_box)
    cont_list_box = decompose_tag(cont_list_box, 'tr', child_tag_attrs={'id':'boardbg'})
    cont_list = extract_children_tag(cont_list_box, 'tr', is_child_multiple=True)
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 and not td_text:
                if var['page_count'] != 1 :
                    break
            if td_idx == 1 :
                onclick = extract_attrs(td, 'onclick')
                href = re.search("'(.+?)'", onclick).group(1)
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 3 :
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
    table_header_box = extract_children_tag(soup, 'tr', child_tag_attrs={'id':'boardbg'})
    cont_list_box = find_parent_tag(table_header_box)
    cont_list_box = decompose_tag(cont_list_box, 'tr', child_tag_attrs={'id':'boardbg'})
    cont_list = extract_children_tag(cont_list_box, 'tr', is_child_multiple=True)
    if cont_list :
        tmp_contents = cont_list[-1]
        var['post_text'] = extract_text(tmp_contents)
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
        var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
