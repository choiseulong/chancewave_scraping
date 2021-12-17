from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                var['postUrl'].append(
                    var['postUrlFrame'] + href
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 2:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText[:-1].replace(' ', ''))
                )
            elif tdIdx == 3:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
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
    content_body = extract_children_tag(soup, 'div', {'class' : 'view_synap'}, childIsNotMultiple)
    dtList = extract_children_tag(content_body, 'dt', dummyAttrs, childIsMultiple)
    for dt in dtList:
        dtText = extract_text(dt)
        if '담당부서' in dtText:
            var['contact'] = dtText
            break
    postText = extract_text(content_body)
    var['postText'] = clean_text(postText)
    imgList = extract_children_tag(content_body, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'base64' in src :
                var['postImageUrl'].append(src)
                continue
            if 'http' not in src :
                src = var['channelMainUrl'] + src
                var['postImageUrl'].append(src)
                continue

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result