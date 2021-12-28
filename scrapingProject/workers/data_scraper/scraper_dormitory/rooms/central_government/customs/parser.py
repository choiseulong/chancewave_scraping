from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['contents_req_params', 'post_title', 'uploaded_time', 'view_count', 'uploader']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    if not tr_list:
        return 
    for tr in tr_list:
        subject = extract_children_tag(tr, 'td', {'data-table' : 'subject'}, DataStatus.not_multiple)
        var['post_title'].append(
            extract_text(subject)
        )
        dataId = extract_attrs(
            extract_children_tag(subject, 'a'),
            'data-id'
        )
        var['contents_req_params'].append(
            {
                "bbsId" : 1341,
                "nttSn" : dataId
            }
        )
        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'date'})
                )
            )
        )
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'number'}, DataStatus.not_multiple)
                )
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'data-table' : 'write'}, DataStatus.not_multiple)
            )
        )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contetns = extract_children_tag(soup, 'td', {'class' : 'conts'}, DataStatus.not_multiple)
    post_text = extract_text(contetns)
    if post_text:
        var['contact'] = extract_contact_numbers_from_text(post_text)
        var['post_text'] = clean_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(contetns, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result