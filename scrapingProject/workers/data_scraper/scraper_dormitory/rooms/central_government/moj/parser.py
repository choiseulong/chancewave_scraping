from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'postSubject', 'uploadedTime', 'uploader', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        trList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for trIdx, tr in enumerate(trList):
            trText = extract_text(tr)
            if trIdx == 1:
                var['postTitle'].append(trText)
                aTag = extract_children_tag(tr, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                var['postUrl'].append(var['channelMainUrl'] + href)
            elif trIdx == 2 : 
                var['postSubject'].append(trText)
            elif trIdx == 3 :
                var['uploader'].append(trText)
            elif trIdx == 5 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(trText)
                )
            elif trIdx == 6 :
                var['viewCount'].append(
                    extract_numbers_in_text(trText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    dtList = extract_children_tag(soup, 'dt', dummyAttrs, childIsMultiple)
    for dt in dtList:
        dtText = extract_text(dt)
        if '전화번호' in dtText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(dt)
                )
            )
            break
    artclView = extract_children_tag(soup, 'div', {'class' : 'artclView'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(artclView))
    imgList = extract_children_tag(artclView, 'img', {'src' : True}, childIsNotMultiple)
    if imgList:
        for img in imgList :
            src = extract_attrs(img, 'src')
            if 'http' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result