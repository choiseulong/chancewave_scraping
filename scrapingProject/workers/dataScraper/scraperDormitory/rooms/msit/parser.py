from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    contentsList = extract_children_tag(soup, 'div', {'class' : 'toggle'}, childIsMultiple)
    for contents in contentsList:
        aTag = extract_children_tag(contents, 'a', dummyAttrs, childIsNotMultiple)
        postId = extract_numbers_in_text(
            extract_attrs(aTag, 'onclick')
        )
        var['postUrl'].append(
            var['postUrlFrame'].format(postId)
        )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'uploader', 'uploadedTime', 'postTitle'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    view_head = extract_children_tag(soup, 'div', {'class' : 'view_head'}, childIsNotMultiple)
    spanList = extract_children_tag(view_head, 'span', {'class' : True}, childIsMultiple)
    var['postTitle'] = extract_text(
        extract_children_tag(view_head, 'h2', dummyAttrs, childIsNotMultiple)
    )
    for span in spanList:
        spanText = extract_text(span)
        if '부서' in spanText or '담당자' in spanText:
            var['uploader'] += extract_text(find_next_tag(span)) + ' '
        elif '연락처' in spanText:
            var['contact'] = extract_contact_numbers_from_text(extract_text(find_next_tag(span)))
        elif '작성일' in spanText:
            var['uploadedTime'] = convert_datetime_string_to_isoformat_datetime(
                    extract_text(find_next_tag(span))
                )
            
    contBox = extract_children_tag(soup, 'div', {'id' : 'cont-wrap'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(contBox))
    imgList = extract_children_tag(contBox, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(result)
    return result