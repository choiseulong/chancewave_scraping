from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    table = extract_children_tag(soup, 'table', child_tag_attrs={'class':'bg_bl'})
    tr_list = extract_children_tag(table, 'tr', is_child_multiple=True)
    if tr_list :
        tr_list = tr_list[3:]
    else :
        return
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list) :
            if td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_title'].append(
                    extract_text(a_tag)
                )
                var['post_url'].append(
                    var['channel_main_url'] + href
                )
            elif td_idx == 2:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(extract_text(td))
                )
    result = merge_var_to_dict(var=var, key_list=key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    li_list = extract_children_tag(soup, 'li', is_child_multiple=True)
    for li in li_list:
        li_text = extract_text(li)
        if '조회수' in li_text :
            var['view_count'] = extract_numbers_in_text(li_text)
            break
    new_contents_common = extract_children_tag(soup, 'div', child_tag_attrs={'class':'new_contents_common'})
    tmp_contents = extract_children_tag(new_contents_common, 'td', child_tag_attrs={'class':'lnb2'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

