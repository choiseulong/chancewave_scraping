from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_url', 'post_title']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_list = extract_children_tag(soup, 'div', child_tag_attrs={'class':'board-list'})
    li_list = extract_children_tag(board_list, 'li', is_child_multiple=True)
    if li_list:
        li_list = li_list[1:]
    else:
        return
    for li in li_list:
        p_title = extract_children_tag(li, 'p', child_tag_attrs={'class':'title'})
        var['post_title'].append(
            extract_text(p_title,)
        )
        post_id = extract_attrs(p_title, 'data-pidx')
        var['post_url'].append(
            var['post_url_frame'].format(post_id)
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text_from_single_tag(li, 'p', child_tag_attrs={'class':'date'})
            )
        )
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view_box = extract_children_tag(soup, 'span', child_tag_attrs={'class' : 'view-view'})
    var['view_count'] = extract_numbers_in_text(extract_text(view_box))
    tmp_contents = extract_children_tag(soup, 'div', child_tag_attrs={'class' : 'view-con'})
    tmp_contents = decompose_tag(tmp_contents, 'div', child_tag_attrs={'class' : 'attachment'})
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    return result