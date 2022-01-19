from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    if not tbody :
        return
    tr_list = extract_children_tag(tbody, 'tr', {'class' : False}, is_child_multiple=True)
    for tr in tr_list :
        title = extract_children_tag(tr, 'a', {'title' : True}, is_child_multiple=False)
        var['post_title'].append(extract_text(title))
        var['post_url'].append(
            var['post_url_frame'].format(extract_text_between_prefix_and_suffix(
                    'dataNo=', '&mode',
                    extract_attrs(
                        title,
                        'href'
                    )
                )
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'class' : 'board_tb_part'}, is_child_multiple=False)
            )
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'board_tb_date'}, is_child_multiple=False)
                )
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'board_tb_hit'}, is_child_multiple=False)
                )
            )
        )
     
    result = merge_var_to_dict(key_list, var)
    # print(result)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    thList = extract_children_tag(tbody, 'th', child_tag_attrs={}, is_child_multiple=True)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(th)
                )
            )
            break
    
    contents = extract_children_tag(tbody, 'td', {'class' : 'con'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(contents))
    var['post_image_url'] = search_img_list_in_contents(contents, var['channel_main_url'])
     
    result = convert_merged_list_to_dict(key_list, var)
    
    # print(result)
    return result