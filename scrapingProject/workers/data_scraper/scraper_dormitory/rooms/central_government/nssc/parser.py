from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : [
            'view_count', 'post_title', 'uploader', 'post_url',
            'uploaded_time', 'contents_req_params', 'post_subject'
        ]
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    pathInfo = {
        'post_title' : '$..SUBJECT', 'uploader': '$..DEPT_NM', 'post_subject' : '$..CATEGORY_NM',
        'view_count' : '$..HITS', 'uploaded_time' : '$..WRITE_DATE'
    }
    postNumber = search_value_in_json_data_using_path(json_data, '$..BBS_SEQ')
    var['contents_req_params'] = [
        {
            "MENU_ID" : 180,
            "SITE_NO" : 2,
            "BOARD_SEQ" : 4, 
            "BBS_SEQ" : num
        } \
        for num \
        in postNumber
    ]
    var['post_url'] = [var['post_url_frame'].format(num) for num in postNumber]
    for key in pathInfo :
        value_list = search_value_in_json_data_using_path(json_data, pathInfo[key])
        if key == 'uploaded_time':
            value_list = [convert_datetime_string_to_isoformat_datetime(date) for date in value_list]
        elif key == 'view_count':
            value_list = [int(count) for count in value_list]
        var[key] = value_list

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text'],
        'multiple_type' : ['post_image_url', 'contact']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    post_text = search_value_in_json_data_using_path(json_data, '$..CONTENTS', 'solo')
    soup = change_to_soup(post_text)
    soupText = extract_text(soup)
    var['post_text'] = clean_text(soupText)
    var['contact'] = extract_contact_numbers_from_text(soupText)
    var['post_image_url'] = search_img_list_in_contents(soup, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
