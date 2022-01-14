from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['contents_req_params', 'post_title', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in tr_list:
        bbs_tit = extract_children_tag(tr, 'td', {'class' : 'bbs_tit'}, is_child_multiple=False)
        a_tag = extract_children_tag(bbs_tit, 'a', {'class' : 'nttInfoBtn'}, is_child_multiple=False)
        dataId = extract_numbers_in_text(
            extract_attrs(
                a_tag, 
                'data-id'
            )
        )
        data = {
            "bbsId" : 1011,
            "nttSn" : dataId
        }
        var['post_title'].append(
            extract_text(a_tag).replace('N', '')
        )
        var['contents_req_params'].append(data)
        
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'date'}, is_child_multiple=False)
                )[:-1]
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'number'}, is_child_multiple=True)[-1]
                )
            )
        )
        
    
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    
    contents = extract_children_tag(soup, 'div', {'class' : 'bbsV_cont'}, is_child_multiple=False)
    var['post_image_url'] = search_img_list_in_contents(contents, var['channel_main_url'])
    post_text = extract_text(contents)
    if post_text:
        var['post_text'] = clean_text(post_text)
        var['contact'] = extract_contact_numbers_from_text(post_text)

    
    result = convert_merged_list_to_dict(key_list, var)
    return result
