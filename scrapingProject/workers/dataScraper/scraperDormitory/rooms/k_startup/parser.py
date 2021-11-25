from workers.dataScraper.scraperDormitory.parserTools.tools import *

childIsMultiple = True
childIsNotMultiple = False
dummpyAttrs = {}

def postListParsingProcess(**params):
    targetKeyInfo = {
        'listType' : ['postSubject', 'postTitle', 'contentsReqParams', 'viewCount', 'uploader', 'endDate']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    CSRF_NONCE = extract_attrs(
        extract_children_tag(soup, 'input', {"name" : "CSRF_NONCE"}, childIsNotMultiple),
        'value'
    )
    tagList = [
        i \
        for i \
        in extract_children_tag(soup, 'li', {'id' : True, 'style' : True, 'class':False}, childIsMultiple)
        if 'liArea' in extract_attrs(i, 'id')
    ]
    for tag in tagList :
        spanList = extract_children_tag(tag, 'span', {"class" : True}, childIsMultiple)
        for span in spanList :
            if 'ann_list_group' in extract_attrs(span, 'class')[0]:
                var['postSubject'].append(extract_text(span))
    var['postTitle'] = [
        extract_text(
            extract_children_tag(tag, 'a')
        ) \
        for tag \
        in tagList
    ]

    for tag in tagList :
        tag = extract_children_tag(tag, 'a', {'style' : True, 'title' : True})
        href = extract_attrs(tag, 'href')
        prefix_length = href.find('(')
        tuple_result = convert_text_to_tuple(href[prefix_length:])
        reqParams = {
            "CSRF_NONCE" : CSRF_NONCE,
            "mid" : 30004,
            "searchPrefixCode" : tuple_result[0],
            "searchPostSn" : tuple_result[1]
        }
        var['contentsReqParams'].append(reqParams)

    infoIdxRoot = {1:'uploader', 2:'endDate', 3:'viewCount'}
    for tag in tagList:
        ann_list_info = extract_children_tag(tag, 'ul', {"class" : "ann_list_info"})
        ann_list_info_li = extract_children_tag(ann_list_info, 'li', dummpyAttrs, childIsMultiple)

        for infoIdx in range(len(ann_list_info_li)) :
            if infoIdx in infoIdxRoot.keys():
                text = extract_text(ann_list_info_li[infoIdx])
                if infoIdx == 3 :
                    text = extract_numbers_in_text(text)
                elif infoIdx == 2 :
                    text = convert_datetime_string_to_isoformat_datetime(text[5:])
                var[infoIdxRoot[infoIdx]].append(
                    text
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'strType' : ['postText', 'contact', 'postContentTarget'],
        'listType' : ['extraInfo']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    var['postText'] = clean_text(
        extract_attrs(
            extract_children_tag(soup, 'meta', {'name' : 'og:description'}, childIsNotMultiple),
            'content'
        ) 
    )
    extraDict = {"infoTitle" : "공고 개요"}
    table = extract_children_tag(soup, 'table', {"class" : ["tbl_gray", "mgb_10"]}, childIsNotMultiple)
    
    th = extract_children_tag(table, 'th', dummpyAttrs, childIsMultiple)
    td = extract_children_tag(table, 'td', dummpyAttrs, childIsMultiple)
    for infoName, infoValue in zip(th, td):
        infoName = extract_text(infoName)
        infoValue = extract_text(infoValue)

        if infoName == '대상': 
            var['postContentTarget'] += "대상:" + infoValue + ' - '
        elif infoName == '대상연령': 
            var['postContentTarget'] += "대상연령:" + infoValue
        elif infoName in ['담당부서', '연락처']:
            var['contact'] += infoValue + ' '
        else :
            extraInfo = [infoName, infoValue]
            extraDict.update({f'info_{len(extraDict)}' : extraInfo})
    var['extraInfo'].append(extraDict)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result 
