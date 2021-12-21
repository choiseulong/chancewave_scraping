from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader', 'postSubject']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    liList = extract_children_tag(soup, 'li', {'class' : 'li1'}, childIsMultiple)
    for li in liList:
        em = extract_children_tag(li, 'em', dummyAttrs, childIsNotMultiple)
        if em:
            postSubject = extract_text(em)[1:-1]
        else :
            postSubject = ''
        var['postSubject'].append(postSubject)
        strong = extract_children_tag(li, 'strong', dummyAttrs, childIsNotMultiple)
        postTitle = extract_text(strong).replace('새 글', '').replace(postSubject, '').strip()
        var['postTitle'].append(postTitle)
        spanList = extract_children_tag(li, 'span', {'class' : 't3'}, childIsMultiple)
        uploader = ''
        for spanIdx, span in enumerate(spanList):
            spanText = extract_text(span)
            if spanIdx == 0:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        spanText
                    )
                )
            elif spanIdx in [1, 2] :
                uploader += spanText + ' '
            elif spanIdx == 3 :
                var['viewCount'].append(
                    extract_numbers_in_text(spanText)
                )
        var['uploader'].append(uploader)
        aTag = extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple)
        href = extract_attrs(aTag, 'href')
        var['postUrl'].append(
            var['postUrlFrame'] + href
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
    info1 = extract_children_tag(soup, 'div', {'class' : 'info1'}, childIsNotMultiple)
    dtList = extract_children_tag(info1, 'dt', dummyAttrs, childIsMultiple)
    for dt in dtList:
        dtText = extract_text(dt)
        if '전화번호' in dtText:
            var['contact'] = extract_contact_numbers_from_text(
                dtText
            )
            break

    substance = extract_children_tag(soup, 'div', {'class' : 'substance'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(substance))
    imgList = extract_children_tag(substance, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    # 이미지 요청시 Referer을 header에 담아 보내야함 
    # Referer = postUrl
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


