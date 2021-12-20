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
    print(result)
    # return result
#### contents 처리해야함
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    info = extract_children_tag(soup, 'div', {'class' : 'info'}, childIsNotMultiple)
    strongList = extract_children_tag(info, 'strong', dummyAttrs, childIsMultiple)
    for strong in strongList:
        strongText = extract_text(strong)
        if '연락처' in strongText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_parent_tag(strong)
                )
            )
            break
    substan = extract_children_tag(soup, 'div', {'class' : 'substan'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(substan))
    imgList = extract_children_tag(substan, 'img', {'src' : True}, childIsMultiple)
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


