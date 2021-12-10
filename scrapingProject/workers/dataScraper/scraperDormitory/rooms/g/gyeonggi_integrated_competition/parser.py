from workers.dataScraper.scraperDormitory.parserTools.tools import *


def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postThumbnail', 'uploadedTime', 'startDate', 'endDate', 'uploader', 'postTitle']
    }
    var, jsonData, keyList = json_type_default_setting(params, targetKeyInfo)
    var['postUrl'] =  [
        var['postUrlFrame'].format(bIdx) \
        for bIdx \
        in search_value_in_json_data_using_path(jsonData, '$..B_IDX')
    ]
    var['postThumbnail'] = [
        var['channelMainUrl'] + img \
        for img \
        in search_value_in_json_data_using_path(jsonData, '$..IMAGE_URL')
    ]
    var['postTitle'] = search_value_in_json_data_using_path(jsonData, '$..SUBJECT')
    var['uploadedTime'] = search_value_in_json_data_using_path(jsonData, '$..WRITE_DATE3')
    var['uploader'] = search_value_in_json_data_using_path(jsonData, '$..ADD_COLUMN06')
    var['startDate'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(jsonData, '$..ADD_COLUMN03')
    ]
    var['endDate'] = [
        convert_datetime_string_to_isoformat_datetime(date) \
        for date \
        in search_value_in_json_data_using_path(jsonData, '$..ADD_COLUMN04')
    ]
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result


def postContentParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['extraInfo', 'postImageUrl', 'linkedPostUrl'],
        'singleType' : ['postContentTarget', 'contact', 'postTextType']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    item_box = extract_children_tag(soup, 'div', {"class" : "item"})
    var['postImageUrl'] = [
        var['channelMainUrl'] + \
        extract_attrs(img, 'src') \
        for img \
        in extract_children_tag(item_box, 'img', dummyAttrs, childIsMultiple)
    ] 

    equitable_box = extract_children_tag(soup, 'div', {"class" : "equitable_box"})
    linkList = extract_children_tag(equitable_box, 'a', dummyAttrs, childIsMultiple)
    if linkList:
        for link in linkList:
            linkHref = extract_attrs(link, 'href')
            if linkHref :
                var['linkedPostUrl'].append(linkHref)
    span_text = [extract_text(span) for span in extract_children_tag(equitable_box, 'span', dummyAttrs, childIsMultiple)]
    p_text = [extract_text(p) for p in extract_children_tag(equitable_box, 'p', dummyAttrs, childIsMultiple)]


    info = {'응모대상' : 'postContentTarget', '문의' : 'contact'}
    extraDict = {'infoTitle' : '공모개요'}

    for tit, cont in zip(span_text, p_text):
        data = [tit, cont]
        for key in info:
            if tit == key:
                var[info[key]] = cont
        dictLength = len(extraDict)
        extraDict.update({f'info_{dictLength}' : data})
    var['extraInfo'].append(extraDict)
    var['postTextType'] = 'onlyExtraInfo'
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result


