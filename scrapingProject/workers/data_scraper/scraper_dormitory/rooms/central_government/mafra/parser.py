from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        a_tag = extract_children_tag(tr, 'a', child_tag_attrs={}, is_child_multiple=False)
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        var['post_title'].append(extract_text(a_tag))
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'dd', {'class' : 'date'}, is_child_multiple=False)
                )
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'dd', {'class' : 'name'}, is_child_multiple=False)
            )
        )

    
    result = merge_var_to_dict(key_list, var)
    # print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'view_count'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view = extract_children_tag(soup, 'div', {'class': 'view'}, is_child_multiple=False)
    var['view_count'] = extract_numbers_in_text(
        extract_text(
            extract_children_tag(view, 'dd', {'class' : 'hit'}, is_child_multiple=False)
        )
    )
    view_contents = extract_children_tag(view, 'div', {'class': 'view_contents'}, is_child_multiple=False)
    post_text = extract_text(view_contents)
    var['post_text'] = clean_text(post_text)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(view_contents, var['channel_main_url'])
     
    result = convert_merged_list_to_dict(key_list, var)
    # print(result)
    return result