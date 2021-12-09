from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    Board_list01 = extract_children_tag(soup, 'div', {'class' : 'Board_list01'}, childIsNotMultiple)
    contents = extract_children_tag(Board_list01, 'ul', dummyAttrs, childIsNotMultiple)
    liList = extract_children_tag(contents, 'li', dummyAttrs, childIsMultiple, isNotRecursive)
    for li in liList:
        spanList = extract_children_tag(li, 'span', dummyAttrs, childIsMultiple)
        for span in spanList:
            spanText = extract_text(span)
            if spanText == '게시일' : 
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        extract_text(
                            find_next_tag(span)
                        )
                    )
                )
            elif spanText == '조회':
                var['viewCount'].append(
                    extract_numbers_in_text(
                        extract_text(
                            find_next_tag(span)
                        )
                    )
                )
        aTag = extract_children_tag(li, 'a', {'class' : 'title'}, childIsNotMultiple)
        var['postTitle'].append(
                clean_text(extract_text(aTag)
            )
        )
        postUrl = extract_attrs(aTag, 'href')
        if 'http' not in postUrl :
            postUrl = var['channelMainUrl'] + postUrl
        var['postUrl'].append(postUrl)
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result


def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'uploader'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    bv_tit_wrap = extract_children_tag(soup, 'div', {'class' : 'bv_tit_wrap'}, childIsNotMultiple)
    liList = extract_children_tag(bv_tit_wrap, 'li', dummyAttrs, childIsMultiple)
    for li in liList:
        spanList = extract_children_tag(li, 'span', dummyAttrs, childIsMultiple)
        for span in spanList:
            spanText = extract_text(span)
            if '담당자' in spanText or '담당부서' in spanText :
                var['uploader'] += extract_text(
                    find_next_tag(span)
                ) + ' '
            elif '전화번호' in spanText :
                var['contact'] = extract_contact_numbers_from_text(
                    extract_text(
                        find_next_tag(span)
                    )
                )
    bv_content_wrap = extract_children_tag(soup, 'div', {'class' : 'bv_content_wrap'}, childIsNotMultiple)
    var['postText'] = extract_text(bv_content_wrap)
    imgList = extract_children_tag(bv_content_wrap, 'img', {'src' : True}, childIsMultiple)
    for img in imgList:
        src = extract_attrs(img, 'src')
        if 'http' not in src :
            src = var['channelMainUrl'] + src
        var['postImageUrl'].append(src)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result