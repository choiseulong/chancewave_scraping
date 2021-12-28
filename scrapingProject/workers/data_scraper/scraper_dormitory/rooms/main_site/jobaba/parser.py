from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'post_thumbnail', 'post_content_target', 'start_date', 'end_date'],
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    var['post_url'] = [
        var['post_url_frame'].format(seq) \
        for seq \
        in search_value_in_json_data_using_path(json_data, '$..seq')
    ]
    var['post_title'] = search_value_in_json_data_using_path(json_data, '$..mainTitle')
    var['post_thumbnail'] = [
        var['channel_main_url'] + thumbParams \
        for thumbParams \
        in search_value_in_json_data_using_path(json_data, '$..thumbImgEncptFileNm')
    ]
    var['post_content_target'] = search_value_in_json_data_using_path(json_data, '$..sprtTrgetDtlApi')
    var['start_date'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(json_data, '$..rqtBgnDe')
    ]
    var['end_date'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(json_data, '$..rqtEndDe')
    ]
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['uploader', 'linked_post_url', 'post_text', 'contact']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    error_warp = extract_children_tag(soup, 'div', {"class" : "error-warp"}, DataStatus.not_multiple)
    if error_warp :
        # 페이지는 있으나 요청에 오류가 발생한 포스트
        return 'retry'

    scripts = extract_children_tag(soup, 'script', DataStatus.empty_attrs, DataStatus.multiple)
    if len(scripts) == 1 :
        # 모집이 마감된 포스트
        return

    mainText = extract_children_tag(soup, 'div', {'class' : 'con-wrap'}, DataStatus.not_multiple)
    if mainText :
        var['post_text'] = clean_text(
                extract_text(
                mainText
            )
        )
    else :
        # 컨텐츠가 없는 포스트
        return 

    linkedPostUrlData = extract_attrs(
        extract_children_tag(soup, 'a', {'class' : 'homepage_go_btn'}, DataStatus.not_multiple),
        'onclick'
    )
    var['linked_post_url'] = extract_values_list_in_both_sides_bracket_text(linkedPostUrlData)[1] if linkedPostUrlData else None
    uploaderData = extract_children_tag(soup, 'p', {'class' : 'note'}, DataStatus.multiple)
    var['uploader'] = extract_text(uploaderData[1]) if uploaderData else None
    var['contact'] = list(set(extract_contact_numbers_from_text(var['post_text']) + extract_emails(var['post_text'])))
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result