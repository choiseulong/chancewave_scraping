from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader', 'postSubject']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    liList = extract_children_tag(soup, 'li', {'class' : 'Lst-Li'}, childIsMultiple)
    for li in liList:
        aTag = extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple)
        href = extract_attrs(aTag, 'href')
        var['postUrl'].append(
            var['channelMainUrl'] + href
        )
        postSubject = extract_text(
                extract_children_tag(li, 'em', dummyAttrs, childIsNotMultiple)
            )
        if postSubject:
            var['postSubject'].append(postSubject[1:-1])
        else :
            var['postSubject'].append(None)
        postTitle = extract_text(
                extract_children_tag(li, 'strong', dummyAttrs, childIsNotMultiple)
            )
        var['postTitle'].append(
            postTitle.replace(postSubject, '')
        )
        infoBox = extract_children_tag(li, 'span', {'class' : 'Lit-DateBx'}, childIsNotMultiple)
        spanList = extract_children_tag(infoBox, 'span', dummyAttrs, childIsMultiple)
        for spanIdx, span in enumerate(spanList) :
            spanText = extract_text(span)
            if spanIdx == 0 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(spanText)
                )
            elif spanIdx == 1 :
                var['uploader'].append(spanText)
            elif spanIdx == 2 :
                var['viewCount'].append(
                    extract_numbers_in_text(spanText)
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
    cont = extract_children_tag(soup, 'div', {'class' : 'cont'}, childIsNotMultiple)
    postText = extract_text(cont)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    imgList = extract_children_tag(cont, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result
