from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import json

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['contact', 'uploader', 'postUrl', 'postTitle', 'postText', 
            'startDate', 'endDate', 'extraInfo']
    }
    var, jsonData, keyList = json_type_default_setting(params, targetKeyInfo)

    var['contact'] = [
        contact if contact else None \
        for contact \
        in search_value_in_json_data_using_path(jsonData, '$..RPRS_CTADR')
    ]
    var['uploader'] = [
        uploader \
        for uploader \
        in search_value_in_json_data_using_path(jsonData, '$..BIZ_CHR_INST_NM')
    ]
    var['postUrl'] = [
        var['postUrlFrame'].format(ID) \
        for ID \
        in search_value_in_json_data_using_path(jsonData, '$..WLFARE_INFO_ID')
    ]
    var['postTitle'] = [
        postTitle \
        for postTitle \
        in search_value_in_json_data_using_path(jsonData, '$..WLFARE_INFO_NM')
    ]
    var['postText'] = [
        postText \
        for postText \
        in search_value_in_json_data_using_path(jsonData, '$..WLFARE_INFO_NM')
    ]
    var['startDate'] = [
        convert_datetime_string_to_isoformat_datetime(startDate) \
        for startDate \
        in search_value_in_json_data_using_path(jsonData, '$..ENFC_BGNG_YMD')
    ]
    var['endDate'] = [
        convert_datetime_string_to_isoformat_datetime(endDate) \
        for endDate \
        in search_value_in_json_data_using_path(jsonData, '$..ENFC_END_YMD')
    ]
    var['extraInfo'] = [
        {
            "infoTitle" : "정책 개요",
            "info_1" : ['추진 지역', location]
        } \
            if location.strip() 
            else {} \
        for location \
        in search_value_in_json_data_using_path(jsonData, '$..ADDR')
    ]
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result



def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postSubject', 'postTextType', 'postText', 'linkedPostUrl']
    }
    var, soup, keyList, text = html_type_default_setting(params, targetKeyInfo)
    textList = [ _.text for _ in extract_children_tag(soup, 'script', dummyAttrs, childIsMultiple) if _.text]
    jsonData = extract_text_list_from_json_data(textList)
    var['postTextType'] = 'both'
    var['postSubject'] = search_value_in_json_data_using_path(jsonData, '$..wlfareInfoReldBztpCdNm', dataIsUnique)
    linkedPostUrl = search_value_in_json_data_using_path(jsonData, '$..etcCn', dataIsUnique)
    var['linkedPostUrl'] = linkedPostUrl if linkedPostUrl else None
    
    postTextCandidateInfo = [
        "wlfareSprtTrgtCn", "aplyMtdDc", "wlfareSprtTrgtSlcrCn", "wlfareSprtBnftCn",\
        "wlfareInfoDtlCn", "bizPrpsCn", "aplyNeedDocCn"
    ]
    textList = []
    for candidate in postTextCandidateInfo:
        var[candidate] = search_value_in_json_data_using_path(jsonData, f'$..{candidate}', dataIsUnique)
        if type(var[candidate]) == type(None):
            continue

        if "</div>" in var[candidate]:
            soupData = change_to_soup(var[candidate])
            childDiv = extract_children_tag(soupData, 'div', dummyAttrs, childIsMultiple)
            for div in childDiv :
                text = clean_text(extract_text(div))
                if text not in textList :
                    textList.append(text)
        else :
            textList.append(clean_text(var[candidate]))
    if textList :
        var['postText'] = '\n'.join(textList) 

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def extract_text_list_from_json_data(textList):
    if textList :
        for i in textList:
            startPoint = 'initParameter('
            endPoint = ');cpr'
            initIndex = i.find(startPoint)
            endIndex = i.find(endPoint)
            if initIndex != -1:
                parsedText = i[initIndex+len(startPoint):endIndex]
                jsonData = json.loads(parsedText)
                dmWlfareInfo = jsonData['initValue']['dmWlfareInfo']
                dmWlfareInfo = json.loads(dmWlfareInfo)
                jsonData['initValue']['dmWlfareInfo'] = dmWlfareInfo
                return jsonData
