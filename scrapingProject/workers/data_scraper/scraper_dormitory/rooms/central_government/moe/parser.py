from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                postId = parse_onclick(
                    extract_attrs(aTag, 'onclick')
                )
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 2 :
                var['uploader'].append(
                    tdText
                )
            elif tdIdx == 3 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 4:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contents = extract_children_tag(soup, 'tr', {'class' : 'BoardTxt'}, childIsNotMultiple)
    postText = extract_text(contents)
    if postText :
        var['contact'] = extract_contact_numbers_from_text(postText)
        var['postText'] = clean_text(postText)
    imgList = extract_children_tag(contents, 'img', {'src' : True}, childIsMultiple)
    for img in imgList:
        src = extract_attrs(img, 'src')
        if 'http' not in src and 'base64' not in src:
            src = var['channelMainUrl'] + src
        var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result