from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'id':'DivContents'})
    table = extract_children_tag(tmp_cont_box, 'table')
    tr_list = extract_children_tag(table, 'tr', is_recursive=False, is_child_multiple=True)
    cont_list = extract_children_tag(tr_list[1], 'tr', is_child_multiple=True)
    if cont_list:
        cont_list = cont_list[2:]
    for cont in cont_list:
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1 :
                onclick = extract_attrs(td, 'onclick')
                href = re.search("'(.+?)'", onclick).group(1)
                var['post_url'].append(
                    var['channel_main_url'] + href
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

    tmp_cont_box = extract_children_tag(soup, 'div', child_tag_attrs={'id':'DivContents'})
    table = extract_children_tag(tmp_cont_box, 'table')
    table = extract_children_tag(table, 'table')
    table = extract_children_tag(table, 'table')
    td_list = extract_children_tag(table, 'td', is_child_multiple=True)
    for td in td_list:
        td_text = extract_text(td)
        if '제목' in td_text:
            var['post_title'] = extract_text(find_next_tag(td))
    tr_list = extract_children_tag(table, 'tr', is_child_multiple=True)
    tmp_contents = tr_list[-1]
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result
