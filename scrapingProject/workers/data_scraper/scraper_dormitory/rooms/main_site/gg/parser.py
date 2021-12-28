from workers.data_scraper.scraper_dormitory.parser_tools.tools import *


def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_thumbnail', 'uploaded_time', 'start_date', 'end_date', 'uploader', 'post_title']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)
    var['post_url'] =  [
        var['post_url_frame'].format(bIdx) \
        for bIdx \
        in search_value_in_json_data_using_path(json_data, '$..B_IDX')
    ]
    var['post_thumbnail'] = [
        var['channel_main_url'] + img \
        for img \
        in search_value_in_json_data_using_path(json_data, '$..IMAGE_URL')
    ]
    var['post_title'] = search_value_in_json_data_using_path(json_data, '$..SUBJECT')
    var['uploaded_time'] = search_value_in_json_data_using_path(json_data, '$..WRITE_DATE3')
    var['uploader'] = search_value_in_json_data_using_path(json_data, '$..ADD_COLUMN06')
    var['start_date'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(json_data, '$..ADD_COLUMN03')
    ]
    var['end_date'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(json_data, '$..ADD_COLUMN04')
    ]
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result


def post_content_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['extra_info', 'post_image_url', 'linked_post_url'],
        'single_type' : ['post_content_target', 'contact', 'post_text_type']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    item_box = extract_children_tag(soup, 'div', {"class" : "item"})
    var['post_image_url'] = [
        var['channel_main_url'] + \
        extract_attrs(img, 'src') \
        for img \
        in extract_children_tag(item_box, 'img', DataStatus.empty_attrs, DataStatus.multiple)
    ] 

    equitable_box = extract_children_tag(soup, 'div', {"class" : "equitable_box"})
    linkList = extract_children_tag(equitable_box, 'a', DataStatus.empty_attrs, DataStatus.multiple)
    if linkList:
        for link in linkList:
            linkHref = extract_attrs(link, 'href')
            if linkHref :
                var['linked_post_url'].append(linkHref)
    span_text = [extract_text(span) for span in extract_children_tag(equitable_box, 'span', DataStatus.empty_attrs, DataStatus.multiple)]
    p_text = [extract_text(p) for p in extract_children_tag(equitable_box, 'p', DataStatus.empty_attrs, DataStatus.multiple)]


    info = {'응모대상' : 'post_content_target', '문의' : 'contact'}
    extraDict = {'info_title' : '공모개요'}

    for tit, cont in zip(span_text, p_text):
        data = [tit, cont]
        for key in info:
            if tit == key:
                var[info[key]] = cont
        dictLength = len(extraDict)
        extraDict.update({f'info_{dictLength}' : data})
    var['extra_info'].append(extraDict)
    var['post_text_type'] = 'only_extra_info'
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result


