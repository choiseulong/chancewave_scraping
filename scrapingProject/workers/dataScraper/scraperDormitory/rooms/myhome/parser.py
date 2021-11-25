from workers.dataScraper.scraperDormitory.parserTools.tools import *

childIsMultiple = True
childIsNotMultiple = False
dummpyAttrs = {}

def postListParsingProcess(**params):
    targetKeyInfo = {
        'listType' : ['isGoingOn', 'postUrl', 'postTitle', 'contact', 'postSubject', 
            'linkedPostUrl', 'startDate', 'endDate', 'uploadedTime',]
    }
    var, jsonData, keyList = json_type_default_setting(params, targetKeyInfo)

    var['isGoingOn'] = [
        True if prgrStts == '모집중' else False \
        for prgrStts \
        in search_value_in_json_data_using_path(jsonData, '$..prgrStts')
    ]
    if not any(var['isGoingOn']):
        # 모든 공고가 모집 완료인 시점에서 종료
        return

    var['postUrl'] = [
        var['postUrlFrame'].format(pblancId) \
        for pblancId \
        in search_value_in_json_data_using_path(jsonData, '$..pblancId')
    ]
    var['postTitle'] = [
        postTitle \
        for postTitle \
        in search_value_in_json_data_using_path(jsonData, '$..pblancNm')
    ]
    var['contact'] = [
        contact \
        for contact \
        in search_value_in_json_data_using_path(jsonData, '$..refrnc')
    ]
    var['postSubject'] = [
        postSubject \
        for postSubject \
        in search_value_in_json_data_using_path(jsonData, '$..suplyInsttNm')
    ]
    var['linkedPostUrl'] = [
        linkedPostUrl \
        for linkedPostUrl \
        in search_value_in_json_data_using_path(jsonData, '$..url')
    ]
    var['startDate'] = [
        parse_frstRegistDt(startDate) \
        for startDate \
        in search_value_in_json_data_using_path(jsonData, '$..rcritPblancDe')
    ]
    var['endDate'] = [
        parse_frstRegistDt(endDate) \
        for endDate \
        in search_value_in_json_data_using_path(jsonData, '$..przwnerPresnatnDe')
    ]
    var['uploadedTime'] = [
        parse_frstRegistDt(uploadedTime)\
        for uploadedTime \
        in search_value_in_json_data_using_path(jsonData, '$..frstRegistDt')
    ]

    valueList = [var[key][:-1] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parse_frstRegistDt(textDate):
    NoneType = type(None)
    if isinstance(textDate, int):
        textDate = str(textDate)
    elif isinstance(textDate, NoneType):
        return 
    year = textDate[:4]
    month = textDate[4:6]
    days = textDate[6:8]
    textDate = f'{year}-{month}-{days}'
    date = convert_datetime_string_to_isoformat_datetime(textDate)
    return date

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'strType' : ['postContentTarget', 'postTextType'],
        'listType' : ['extraInfo']
    }
    var, soup, keyList, text = html_type_default_setting(params, targetKeyInfo)

    var['postContentTarget'] = '-'.join(
        [extract_text(tag) for tag in extract_children_tag(soup, 'span', {'class' : 'ds'}, childIsMultiple)]
    )
    var['postTextType'] = 'onlyExtraInfo'
    extraDict = {'infoTitle' : '공고 개요'}
    div_info = extract_children_tag(soup, 'div', {'class' : 'info'}, childIsNotMultiple)
    for title, value in zip(
        extract_children_tag(div_info, 'dt', dummpyAttrs, childIsMultiple), 
        extract_children_tag(div_info, 'dd', dummpyAttrs, childIsMultiple), 
    ):
        title = extract_text(title)
        value = extract_text(value)
        extraDictLenth = len(extraDict)
        extraDict.update({f'info_{extraDictLenth}' : [title, value]})
    var['extraInfo'].append(extraDict)

    extraDict = {'infoTitle' : '단지 정보'}
    addressList, firstEntryDateList = extract_info(text)
    extraDict.update({'info_0' : ['주소', addressList]})
    extraDict.update({'info_1': ['최초 입주 년월', firstEntryDateList]})
    var['extraInfo'].append(extraDict)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def extract_info(text):
    split_text = text[text.find('//단지변경이벤트'):text.find('//공급변경이벤트')]
    infoList = [i for i in [txt.split('(')[0] for txt in split_text.strip().split('({')][1:]]
    addressList = []
    firstEntryDateList = []
    for infoText in infoList :
        idxList = search_prefix_and_suffix_idx(infoText)
        contentsInfo = [infoText[preIdx+1: sufIdx].strip() for preIdx, sufIdx in idxList]
        address = contentsInfo[2].replace('\\', '').replace('"', '')
        addressList.append(address)
        firstEntryDate = contentsInfo[4] + '년 '+ contentsInfo[5] + '월'
        firstEntryDateList.append(firstEntryDate.replace('\\', '').replace('"', ''))
    return addressList, firstEntryDateList

def search_prefix_and_suffix_idx(text):
    prefixIndex = [idx for idx, _ in enumerate(text) if _ == ':']
    suffixIndex = [idx for idx, _ in enumerate(text) if _ == ','] + [len(text)]
    return zip(prefixIndex, suffixIndex)
