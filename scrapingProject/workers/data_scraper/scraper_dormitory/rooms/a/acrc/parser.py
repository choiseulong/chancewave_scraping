from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'uploadedTime', 'postUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    contentsBox = extract_children_tag(soup, 'table', {'class' : 'boardList'}, childIsNotMultiple)
    tbody = extract_children_tag(contentsBox, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 0 :
                if '공지' == tdText:
                    break
            elif tdIdx == 1 :
                var['postTitle'].append(tdText)
                href = extract_attrs(
                    extract_children_tag(td, 'a', {'href' : True}, childIsNotMultiple),
                    'href'
                )
                if 'http' not in href :
                    href = var['channelMainUrl'] + href
                var['postUrl'].append(href)
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 5 :
                var['viewCount'].append(extract_numbers_in_text(tdText))

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText'],
        'multipleType' : ['postImageUrl', 'contact']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    viewContent = extract_children_tag(soup, 'div', {'class' : 'viewContent'}, childIsNotMultiple)
    postText = extract_text(viewContent)
    if postText:
        var['postText'] = clean_text(postText)
        var['contact'] = extract_contact_numbers_from_text(postText)
    imgList = extract_children_tag(viewContent, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList :
            src = extract_attrs(img, 'src')
            if 'http' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
            
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
