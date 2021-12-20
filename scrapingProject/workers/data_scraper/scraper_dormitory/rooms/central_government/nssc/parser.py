from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : [
            'viewCount', 'postTitle', 'uploader', 'postUrl',
            'uploadedTime', 'contentsReqParams', 'postSubject'
        ]
    }
    var, jsonData, keyList = json_type_default_setting(params, targetKeyInfo)
    pathInfo = {
        'postTitle' : '$..SUBJECT', 'uploader': '$..DEPT_NM', 'postSubject' : '$..CATEGORY_NM',
        'viewCount' : '$..HITS', 'uploadedTime' : '$..WRITE_DATE'
    }
    postNumber = search_value_in_json_data_using_path(jsonData, '$..BBS_SEQ')
    var['contentsReqParams'] = [
        {
            "MENU_ID" : 180,
            "SITE_NO" : 2,
            "BOARD_SEQ" : 4, 
            "BBS_SEQ" : num
        } \
        for num \
        in postNumber
    ]
    var['postUrl'] = [var['postUrlFrame'].format(num) for num in postNumber]
    for key in pathInfo :
        valueList = search_value_in_json_data_using_path(jsonData, pathInfo[key])
        if key == 'uploadedTime':
            valueList = [convert_datetime_string_to_isoformat_datetime(date) for date in valueList]
        elif key == 'viewCount':
            valueList = [int(count) for count in valueList]
        var[key] = valueList

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText'],
        'multipleType' : ['postImageUrl', 'contact']
    }
    var, jsonData, keyList = json_type_default_setting(params, targetKeyInfo)

    postText = search_value_in_json_data_using_path(jsonData, '$..CONTENTS', 'solo')
    soup = change_to_soup(postText)
    soupText = extract_text(soup)
    var['postText'] = clean_text(soupText)
    var['contact'] = extract_contact_numbers_from_text(soupText)
    imgList = extract_children_tag(soup, 'img', {'src' : True}, childIsNotMultiple)
    if imgList:
        for img in imgList :
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
