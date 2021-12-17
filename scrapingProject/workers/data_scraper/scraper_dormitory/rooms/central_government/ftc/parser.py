from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'uploadedTime', 'contentsReqParams']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsMultiple)
    if len(tbody):
        tbody = tbody[1]
    contentsBox = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for contents in contentsBox:
        tdList = extract_children_tag(contents, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                var['postTitle'].append(tdText) 
                nttId = parse_href(
                    extract_attrs(
                        extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple),
                        'onclick'
                    )
                )
                data = {
                    "bbsId" : "BBSMSTR_000000002424",
                    "bbsTyCode" : "BBST01",
                    "nttId" : nttId,
                    "pageIndex" : 1
                }
                var['contentsReqParams'].append(
                    data
                )
            elif tdIdx == 2:
                var['uploader'].append(tdText)
            elif tdIdx == 3:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        tdText
                    )
                )
            elif tdIdx == 5 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
            else :
                continue

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parse_href(text):
    prefix = "('"
    suffix = "')"
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result

    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText'],
        'multipleType' : ['postImageUrl', 'contact']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contents = extract_children_tag(soup, 'td', {'class' : 'bbs_content'}, childIsNotMultiple)
    postText = extract_text(contents)
    if postText:
        var['postText'] = clean_text(postText)
        var['contact'] = extract_contact_numbers_from_text(postText)
    imgList = extract_children_tag(contents, 'img', dummyAttrs, childIsMultiple)
    if imgList :
        for img in imgList:
            href = extract_attrs(img, 'href')
            if 'http' not in href:
                href = var['channelMainUrl'] + href
            var['postImageUrl'].append(href)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
