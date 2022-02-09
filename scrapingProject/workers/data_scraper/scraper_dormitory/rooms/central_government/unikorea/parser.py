from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'view_count', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    if not tr_list:
        return
    for tr in tr_list:
        title = extract_children_tag(tr, 'td', {'class' : 'title'}, is_child_multiple=False)
        var['post_title'].append(extract_text(title))
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'created'}, is_child_multiple=False)
                )
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'hit'}, is_child_multiple=False)
                )
            )
        )
        postId = extract_text_between_prefix_and_suffix(
            'cntId=', 
            '&amp', 
            extract_attrs(
                extract_children_tag(title, 'a', child_tag_attrs={}, is_child_multiple=False),
                'href'
            )
        )
        var['post_url'].append(
            var['post_url_frame'].format(postId)
        )

    
    result = merge_var_to_dict(key_list, var)
    
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    board_content = extract_children_tag(soup, 'div', {'class' : 'board_content'}, is_child_multiple=False)
    post_text = extract_text(board_content)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_text'] = clean_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(board_content, var['channel_main_url'])
    
    result = convert_merged_list_to_dict(key_list, var)
    
    return result