from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    data_list = json_data['data']
    for data in data_list:
        var['post_title'].append(
            data['서비스명']
        )
        var['post_url'].append(
            var['post_url_frame'].format(data['서비스ID'])
        )
    result = merge_var_to_dict(key_list, var)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_content_target'],
        'multiple_type' : ['extra_info']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    extra_info = {'info_title' : '상세정보'}
    data = json_data['data'][0]
    for key in data:
        if '전화번호' in key:
            var['contact'] = data[key]
        elif '서비스목적' in key :
            var['post_text'] = clean_text(data[key])
        elif '기관명' in key :
            var['uploader'] = data[key]
        elif '지원대상' in key :
            var['post_content_target'] = data[key]
        else :
            extra_info.update({key : data[key]})
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    return result

