from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['uploaded_time', 'post_title', 'view_count', 'contents_req_params']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    path_info = {
        '$..TITL_NM':'post_title',
        '$..CATG_CD':'post_subject',
        '$..REG_DTM':'uploaded_time',
        '$..SLNO':'contents_req_params',
        '$..INQ_NCNT':'view_count'
    }
    data_list = search_value_in_json_data_using_path(json_data, path_info)
    for path_idx, path in enumerate(path_info.keys()) :
        if path == '$..INQ_NCNT':
            data_list[path_idx] = [int(i) for i in data_list[path_idx]]
        var[path_info[path]] = data_list[path_idx]
    var['contents_req_params'] = [
        {
            "searchG":"titleCon",
            "param":"proc=View",
            "seqNo":post_id
        } \
        for post_id \
        in var['contents_req_params']
    ]
    var['uploaded_time'] = [convert_datetime_string_to_isoformat_datetime(date) for date in var['uploaded_time']]
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
    }
    var, json_data, key_list,  = json_type_default_setting(params, target_key_info)
    tmp_contents = search_value_in_json_data_using_path(json_data, '$..TTU_TXT', is_data_multiple=False)
    var['post_text'] = erase_html_tags(
        tmp_contents
    )
    var['contact'] = extract_contact_numbers_from_text(tmp_contents)
    
    result = convert_merged_list_to_dict(key_list, var)
    return result

