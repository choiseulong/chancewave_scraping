from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import json

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['contact', 'uploader', 'post_url', 'post_title', 'post_text', 
            'start_date', 'end_date', 'extra_info']
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    var['contact'] = [
        contact if contact else None \
        for contact \
        in search_value_in_json_data_using_path(json_data, '$..RPRS_CTADR')
    ]
    var['uploader'] = [
        uploader \
        for uploader \
        in search_value_in_json_data_using_path(json_data, '$..BIZ_CHR_INST_NM')
    ]
    var['post_url'] = [
        var['post_url_frame'].format(ID) \
        for ID \
        in search_value_in_json_data_using_path(json_data, '$..WLFARE_INFO_ID')
    ]
    var['post_title'] = [
        post_title \
        for post_title \
        in search_value_in_json_data_using_path(json_data, '$..WLFARE_INFO_NM')
    ]
    var['post_text'] = [
        post_text \
        for post_text \
        in search_value_in_json_data_using_path(json_data, '$..WLFARE_INFO_NM')
    ]
    var['start_date'] = [
        convert_datetime_string_to_isoformat_datetime(start_date) \
        for start_date \
        in search_value_in_json_data_using_path(json_data, '$..ENFC_BGNG_YMD')
    ]
    var['end_date'] = [
        convert_datetime_string_to_isoformat_datetime(end_date) \
        for end_date \
        in search_value_in_json_data_using_path(json_data, '$..ENFC_END_YMD')
    ]
    var['extra_info'] = [
        {
            "info_title" : "정책 개요",
            "info_1" : ['추진 지역', location]
        } \
            if location.strip() 
            else {} \
        for location \
        in search_value_in_json_data_using_path(json_data, '$..ADDR')
    ]
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result



def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_subject', 'post_text_type', 'post_text', 'linked_post_url']
    }
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)
    textList = [ _.text for _ in extract_children_tag(soup, 'script', DataStatus.empty_attrs, DataStatus.multiple) if _.text]
    json_data = extract_text_list_from_json_data(textList)
    var['post_text_type'] = 'both'
    var['post_subject'] = search_value_in_json_data_using_path(json_data, '$..wlfareInfoReldBztpCdNm', DataStatus.unique)
    linked_post_url = search_value_in_json_data_using_path(json_data, '$..etcCn', DataStatus.unique)
    var['linked_post_url'] = linked_post_url if linked_post_url else None
    
    postTextCandidateInfo = [
        "wlfareSprtTrgtCn", "aplyMtdDc", "wlfareSprtTrgtSlcrCn", "wlfareSprtBnftCn",\
        "wlfareInfoDtlCn", "bizPrpsCn", "aplyNeedDocCn"
    ]
    textList = []
    for candidate in postTextCandidateInfo:
        var[candidate] = search_value_in_json_data_using_path(json_data, f'$..{candidate}', DataStatus.unique)
        if type(var[candidate]) == type(None):
            continue

        if "</div>" in var[candidate]:
            soupData = change_to_soup(var[candidate])
            childDiv = extract_children_tag(soupData, 'div', DataStatus.empty_attrs, DataStatus.multiple)
            for div in childDiv :
                text = clean_text(extract_text(div))
                if text not in textList :
                    textList.append(text)
        else :
            textList.append(clean_text(var[candidate]))
    if textList :
        var['post_text'] = '\n'.join(textList) 

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
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
                json_data = json.loads(parsedText)
                dmWlfareInfo = json_data['initValue']['dmWlfareInfo']
                dmWlfareInfo = json.loads(dmWlfareInfo)
                json_data['initValue']['dmWlfareInfo'] = dmWlfareInfo
                return json_data
