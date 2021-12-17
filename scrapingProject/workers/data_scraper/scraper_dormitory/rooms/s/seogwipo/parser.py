from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'postUrl', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', {}, childIsNotMultiple)
    trList_all = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    trList_info = extract_children_tag(tbody, 'tr', {'class' : 'info'}, childIsMultiple)
    validTrList = list(set(trList_all) - set(trList_info))
    for tr in validTrList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1 :
                var['postUrl'].append(
                    var['channelMainUrl'] + \
                    extract_attrs(
                        extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple), 'href'
                    )
                )
                var['postTitle'].append(
                    tdText
                )
            elif tdIdx == 3:
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        tdText
                    )
                )
            elif tdIdx == 5 :
                var['viewCount'].append(extract_numbers_in_text(tdText))

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    viewContent = extract_children_tag(soup, 'div', {'class':'view-contents'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(viewContent))
    imgList = extract_children_tag(viewContent, 'img', dummyAttrs, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'html' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
