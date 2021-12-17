from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'postUrl', 'postSubject', 'isGoingOn']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    contentsList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for contents in contentsList:
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(contents, 'td', {'class' : 'hit'}, childIsNotMultiple)
                )
            )
        )
        var['postTitle'].append(
            extract_text(
                extract_children_tag(contents, 'p', {'class' : 'title'}, childIsNotMultiple)
            )
        )
        var['postSubject'].append(
            extract_text(
                extract_children_tag(contents, 'div', {'class' : 'hashtag'}, childIsNotMultiple)
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(contents, 'td', dummyAttrs, childIsMultiple)[1]
            )
        )
        var['postUrl'].append(
            var['channelMainUrl'] + \
            extract_attrs(
                extract_children_tag(contents, 'a', {'href' : True}, childIsNotMultiple),
                'href'
            )
        )
        stateText = extract_text(
                extract_children_tag(contents, 'span', {'class' : 'state'}, childIsNotMultiple)
            )
        var['isGoingOn'].append(
            True if stateText != '모집마감' else False
        )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postSubject', 'linkedPostUrl', 'startDate', 'endDate', 'postTextType'],
        'multipleType' : ['extraInfo']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    extraDict = {'infoTitle':'장학 개요'}
    var['postTextType'] = 'onlyExtraInfo'
    
    infoTable = extract_children_tag(soup, 'div', {'class' : 'infoTable'}, childIsNotMultiple)
    info_ul = extract_children_tag(infoTable, 'ul', dummyAttrs, childIsMultiple)
    for ul in info_ul:
        ulData = extract_children_tag(ul, 'li', dummyAttrs, childIsMultiple)
        ulText = [clean_text(extract_text(i)) for i in ulData]
        if ulText[0] == '장학종류' :
            var['postSubject'] = ulText[1]
        elif ulText[0] == '원문공고' :
            var['linkedPostUrl'] = parse_linkedPostUrl(
                extract_attrs(
                    extract_children_tag(ulData[1], 'a', {'href' : True}, childIsNotMultiple),
                    'href'
                )
            )
        elif ulText[0] == '신청기간':
            var['startDate'], var['endDate'] = parse_date(ulText[1])
        else :
            lenExtraDict = len(extraDict)
            extraDict.update({f'info_{lenExtraDict}' : ulText})

    main_content = extract_children_tag(soup, 'div', {"id" : "t_content"}) 
    pTagList = extract_children_tag(main_content, 'p', dummyAttrs, childIsMultiple)
    pTagTextList = [extract_text(p) for p in pTagList]
    valueList = parse_ptag_info(pTagTextList)
    for value in valueList:
        lenExtraDict = len(extraDict)
        extraDict.update({f'info_{lenExtraDict}' : value})
    var['extraInfo'].append(extraDict)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def parse_ptag_info(pTagTextList):
    titleIdx = [idx for idx, _ in enumerate(pTagTextList) if '•' in _ ]
    valueList = [pTagTextList[titleIdx[i]:titleIdx[i+1]] for i in range(len(titleIdx)-1)]
    for valueIdx, value in enumerate(valueList) :
        valueList[valueIdx] = [clean_text(value[0])[2:], clean_text(' '.join(value[1:]))]
    return valueList

def parse_linkedPostUrl(text):
    return text[text.find('http'): text.rfind("',")]

def parse_date(text):
    date = [
        convert_datetime_string_to_isoformat_datetime(i[:-5].replace(' ', '')) \
        for i \
        in text.split(' ~ ')
    ]
    return date[0], date[1]