from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['is_going_on', 'post_url', 'post_title', 'contact', 'post_subject', 
            'linked_post_url', 'start_date', 'end_date', 'uploaded_time',]
    }
    var, json_data, key_list = json_type_default_setting(params, target_key_info)

    var['is_going_on'] = [
        True if prgrStts == '모집중' else False \
        for prgrStts \
        in search_value_in_json_data_using_path(json_data, '$..prgrStts')
    ]
    if not any(var['is_going_on']):
        # 모든 공고가 모집 완료인 시점에서 종료
        return

    var['post_url'] = [
        var['post_url_frame'].format(pblancId) \
        for pblancId \
        in search_value_in_json_data_using_path(json_data, '$..pblancId')
    ]
    var['post_title'] = [
        post_title \
        for post_title \
        in search_value_in_json_data_using_path(json_data, '$..pblancNm')
    ]
    var['contact'] = [
        contact \
        for contact \
        in search_value_in_json_data_using_path(json_data, '$..refrnc')
    ]
    var['post_subject'] = [
        post_subject \
        for post_subject \
        in search_value_in_json_data_using_path(json_data, '$..suplyInsttNm')
    ]
    var['linked_post_url'] = [
        linked_post_url \
        for linked_post_url \
        in search_value_in_json_data_using_path(json_data, '$..url')
    ]
    var['start_date'] = [
        parse_frstRegistDt(start_date) \
        for start_date \
        in search_value_in_json_data_using_path(json_data, '$..rcritPblancDe')
    ]
    var['end_date'] = [
        parse_frstRegistDt(end_date) \
        for end_date \
        in search_value_in_json_data_using_path(json_data, '$..przwnerPresnatnDe')
    ]
    var['uploaded_time'] = [
        parse_frstRegistDt(uploaded_time)\
        for uploaded_time \
        in search_value_in_json_data_using_path(json_data, '$..frstRegistDt')
    ]

    value_list = [var[key][:-1] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
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

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_content_target', 'post_text_type'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, text = html_type_default_setting(params, target_key_info)

    var['post_content_target'] = '-'.join(
        [extract_text(tag) for tag in extract_children_tag(soup, 'span', {'class' : 'ds'}, DataStatus.multiple)]
    )
    var['post_text_type'] = 'only_extra_info'
    extraDict = {'info_title' : '공고 개요'}
    div_info = extract_children_tag(soup, 'div', {'class' : 'info'}, DataStatus.not_multiple)
    for title, value in zip(
        extract_children_tag(div_info, 'dt', DataStatus.empty_attrs, DataStatus.multiple), 
        extract_children_tag(div_info, 'dd', DataStatus.empty_attrs, DataStatus.multiple), 
    ):
        title = extract_text(title)
        value = extract_text(value)
        extraDictLenth = len(extraDict)
        extraDict.update({f'info_{extraDictLenth}' : [title, value]})
    var['extra_info'].append(extraDict)

    extraDict = {'info_title' : '단지 정보'}
    addressList, firstEntryDateList = extract_info(text)
    extraDict.update({'info_0' : ['주소', addressList]})
    extraDict.update({'info_1': ['최초 입주 년월', firstEntryDateList]})
    var['extra_info'].append(extraDict)
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
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
