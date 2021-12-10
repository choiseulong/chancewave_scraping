from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'postThumbnail', 'postContentTarget', 'startDate', 'endDate'],
    }
    var, jsonData, keyList = json_type_default_setting(params, targetKeyInfo)
    var['postUrl'] = [
        var['postUrlFrame'].format(seq) \
        for seq \
        in search_value_in_json_data_using_path(jsonData, '$..seq')
    ]
    var['postTitle'] = search_value_in_json_data_using_path(jsonData, '$..mainTitle')
    var['postThumbnail'] = [
        var['channelMainUrl'] + thumbParams \
        for thumbParams \
        in search_value_in_json_data_using_path(jsonData, '$..thumbImgEncptFileNm')
    ]
    var['postContentTarget'] = search_value_in_json_data_using_path(jsonData, '$..sprtTrgetDtlApi')
    var['startDate'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(jsonData, '$..rqtBgnDe')
    ]
    var['endDate'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(jsonData, '$..rqtEndDe')
    ]
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['uploader', 'linkedPostUrl', 'postText', 'contact']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    error_warp = extract_children_tag(soup, 'div', {"class" : "error-warp"}, childIsNotMultiple)
    if error_warp :
        # 페이지는 있으나 요청에 오류가 발생한 포스트
        return 'retry'

    scripts = extract_children_tag(soup, 'script', dummyAttrs, childIsMultiple)
    if len(scripts) == 1 :
        # 모집이 마감된 포스트
        return

    mainText = extract_children_tag(soup, 'div', {'class' : 'con-wrap'}, childIsNotMultiple)
    if mainText :
        var['postText'] = clean_text(
                extract_text(
                mainText
            )
        )
    else :
        # 컨텐츠가 없는 포스트
        return 

    linkedPostUrlData = extract_attrs(
        extract_children_tag(soup, 'a', {'class' : 'homepage_go_btn'}, childIsNotMultiple),
        'onclick'
    )
    var['linkedPostUrl'] = extract_values_list_in_both_sides_bracket_text(linkedPostUrlData)[1] if linkedPostUrlData else None
    uploaderData = extract_children_tag(soup, 'p', {'class' : 'note'}, childIsMultiple)
    var['uploader'] = extract_text(uploaderData[1]) if uploaderData else None
    var['contact'] = list(set(extract_contact_numbers_from_text(var['postText']) + extract_emails(var['postText'])))
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result