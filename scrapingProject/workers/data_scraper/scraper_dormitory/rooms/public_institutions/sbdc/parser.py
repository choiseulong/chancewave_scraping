from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploader']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    path_info = {
        '$..subject' : 'post_title',
        '$..writer' : 'uploader',
        '$..articleKey' : 'post_url'
    }
    data_list = search_value_in_json_data_using_path(json_data, path_info)
    for path_idx, path in enumerate(path_info):
        var[path_info[path]] = data_list[path_idx]
    var['post_url'] = [var['post_url_frame'].format(post_id) for post_id in var['post_url']]
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'uploaded_time'],
        'multiple_type' : ['post_image_url']
    }
    var, json_data, key_list, = json_type_default_setting(params, target_key_info)
    tmp_contents = search_value_in_json_data_using_path(json_data, '$..content1', is_data_multiple=False)
    tmp_contents = change_to_soup(tmp_contents)
    var['post_text'] = extract_text(tmp_contents)
    var['contact'] = extract_contact_numbers_from_text(extract_text(tmp_contents)) 
    var['post_image_url'] = search_img_list_in_contents(tmp_contents, var['channel_main_url'])
    date = search_value_in_json_data_using_path(json_data, '$..regDate', is_data_multiple=False)
    var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(date[:8])
    result = convert_merged_list_to_dict(key_list, var)
    return result

