from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    nothing = extract_children_tag(soup, 'li', child_tag_attrs={'class':'nothing'})
    if nothing:
        return
    cont_box = extract_children_tag(soup, 'ul', child_tag_attrs={'class':'news_list_box'})
    cont_list = extract_children_tag(cont_box, 'li', is_child_multiple=True, is_recursive=False)
    for cont in cont_list:
        notice_text = extract_text_from_single_tag(cont, 'div', child_tag_attrs={'class':'num_area'})
        if '공지' in notice_text and var['page_count'] != 1 :
            continue
        var['post_title'].append(
            extract_text_from_single_tag(cont, 'div', child_tag_attrs={'class':'subject'})
        )
        var['uploader'].append(
            extract_text_from_single_tag(cont, 'li', child_tag_attrs={'class':'writer'})
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(cont, 'li', child_tag_attrs={'class':'date'})
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text_from_single_tag(cont, 'li', child_tag_attrs={'class':'view'})
            )
        )
        a_tag = extract_children_tag(cont, 'a')
        onclick = extract_attrs(a_tag, 'onclick')
        post_id = parse_post_id(onclick, [0,1])
        var['post_url'].append(
            var['post_url_frame'].format(post_id[0], post_id[1])
        )

    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class':'txt_in'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    result = convert_merged_list_to_dict(key_list, var)
    return result

