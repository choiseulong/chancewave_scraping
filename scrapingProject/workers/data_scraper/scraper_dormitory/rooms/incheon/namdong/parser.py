from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    title_list = extract_children_tag(soup, 'p', child_tag_attrs={'class':'title'}, is_child_multiple=True)
    for title in title_list:
        a_tag = extract_children_tag(title, 'a')
        href = extract_attrs(a_tag, 'href') 
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
    info_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'writer_info'}, is_child_multiple=True)
    for info in info_list:
        var['uploader'].append(
            extract_text_from_single_tag(info, 'li', child_tag_attrs={'title':'작성자'})
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(info, 'li', child_tag_attrs={'title':'작성일'})
            )
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact',],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    dt_list = extract_children_tag(soup, 'dt', is_child_multiple=True)
    for dt in dt_list:
        dt_text = extract_text(dt)
        if '전화번호' in dt_text:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(dt)
                )
            )
            break
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'con'})
    tmp_contents = decompose_tag(tmp_contents, 'p', child_tag_attrs={'class':'openNuri'})
    var['post_text'] = extract_text(tmp_contents)
    if not var['contact']:
        var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

