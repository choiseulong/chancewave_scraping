from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'postUrl', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    mainDiv = extract_children_tag(soup, 'div', {'class' : 'bbs_list01'}, childIsNotMultiple)
    if '0' in var['channelCode']:
        ulList = extract_children_tag(mainDiv, 'ul', dummyAttrs, childIsMultiple, isNotRecursive)
        if len(ulList):
            ulList = ulList[1]
    else :
        ulList = extract_children_tag(mainDiv, 'ul', dummyAttrs, childIsNotMultiple)

    var['uploadedTime'] = [
        convert_datetime_string_to_isoformat_datetime(
            extract_text(i)
        )
        for i \
        in extract_children_tag(ulList, 'div', {'class' : 'right_column'}, childIsMultiple)
    ]
    aTagList = [
        aTag for aTag in extract_children_tag(ulList, 'a', dummyAttrs, childIsMultiple) \
        if 'title' in extract_attrs(aTag, 'class')
    ]
    for aTag in aTagList:
        href = extract_attrs(aTag, 'href')
        if 'html' not in href:
            href = parse_href(href)
            href = var['postUrlFrame'].format(href)
        var['postUrl'].append(href)
        var['postTitle'].append(extract_text(aTag))

    winfoList = extract_children_tag(ulList, 'div', {"class" : "winfo"}, childIsMultiple)
    for winfo in winfoList:
        pTagList = extract_children_tag(winfo, 'p', dummyAttrs, childIsMultiple)
        for pTag in pTagList:
            pText = extract_text(pTag)
            if '담당부서' in pText:
                var['uploader'].append(pText.split(' | ')[1])
            elif '조회수' in pText:
                var['viewCount'].append(
                    extract_numbers_in_text(pText)
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parse_href(text):
    prefix = 'seq='
    suffix = '&amp'
    return text[text.find(prefix) + len(prefix) : text.find(suffix)]
    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'contact'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contentBox = extract_children_tag(soup, 'div', {'class' : 'bv_cont'}, childIsNotMultiple)
    contactBox = extract_children_tag(soup, 'div', {'class' : 'bbs_sat_header'}, childIsNotMultiple)
    spanList = extract_children_tag(contactBox, 'span', dummyAttrs, childIsMultiple)
    if spanList:
        for span in spanList:
            spanText = extract_text(span)
            var['contact'] += spanText + ' '
        var['postText'] = extract_text(contentBox)
    imgBox = extract_children_tag(contentBox, 'img', dummyAttrs, childIsMultiple)
    if imgBox:
        for img in imgBox:
            src = extract_attrs(img,'src')
            if 'html' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result