from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'post_url', 'post_subject', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.not_multiple)
    contentsList = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for contents in contentsList:
        var['view_count'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(contents, 'td', {'class' : 'hit'}, DataStatus.not_multiple)
                )
            )
        )
        var['post_title'].append(
            extract_text(
                extract_children_tag(contents, 'p', {'class' : 'title'}, DataStatus.not_multiple)
            )
        )
        var['post_subject'].append(
            extract_text(
                extract_children_tag(contents, 'div', {'class' : 'hashtag'}, DataStatus.not_multiple)
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(contents, 'td', DataStatus.empty_attrs, DataStatus.multiple)[1]
            )
        )
        var['post_url'].append(
            var['channel_main_url'] + \
            extract_attrs(
                extract_children_tag(contents, 'a', {'href' : True}, DataStatus.not_multiple),
                'href'
            )
        )
        stateText = extract_text(
                extract_children_tag(contents, 'span', {'class' : 'state'}, DataStatus.not_multiple)
            )
        var['is_going_on'].append(
            True if stateText != '모집마감' else False
        )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_subject', 'linked_post_url', 'start_date', 'end_date', 'post_text_type'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    extraDict = {'info_title':'장학 개요'}
    var['post_text_type'] = 'only_extra_info'
    
    infoTable = extract_children_tag(soup, 'div', {'class' : 'infoTable'}, DataStatus.not_multiple)
    info_ul = extract_children_tag(infoTable, 'ul', DataStatus.empty_attrs, DataStatus.multiple)
    for ul in info_ul:
        ulData = extract_children_tag(ul, 'li', DataStatus.empty_attrs, DataStatus.multiple)
        ulText = [clean_text(extract_text(i)) for i in ulData]
        if ulText[0] == '장학종류' :
            var['post_subject'] = ulText[1]
        elif ulText[0] == '원문공고' :
            var['linked_post_url'] = parse_linkedPostUrl(
                extract_attrs(
                    extract_children_tag(ulData[1], 'a', {'href' : True}, DataStatus.not_multiple),
                    'href'
                )
            )
        elif ulText[0] == '신청기간':
            var['start_date'], var['end_date'] = parse_date(ulText[1])
        else :
            lenExtraDict = len(extraDict)
            extraDict.update({f'info_{lenExtraDict}' : ulText})

    main_content = extract_children_tag(soup, 'div', {"id" : "t_content"}) 
    pTagList = extract_children_tag(main_content, 'p', DataStatus.empty_attrs, DataStatus.multiple)
    pTagTextList = [extract_text(p) for p in pTagList]
    value_list = parse_ptag_info(pTagTextList)
    for value in value_list:
        lenExtraDict = len(extraDict)
        extraDict.update({f'info_{lenExtraDict}' : value})
    var['extra_info'].append(extraDict)
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result

def parse_ptag_info(pTagTextList):
    titleIdx = [idx for idx, _ in enumerate(pTagTextList) if '•' in _ ]
    value_list = [pTagTextList[titleIdx[i]:titleIdx[i+1]] for i in range(len(titleIdx)-1)]
    for valueIdx, value in enumerate(value_list) :
        value_list[valueIdx] = [clean_text(value[0])[2:], clean_text(' '.join(value[1:]))]
    return value_list

def parse_linkedPostUrl(text):
    return text[text.find('http'): text.rfind("',")]

def parse_date(text):
    if '2차' in text:
        text = [i for i in text.split(' ') if '.' in i]
        text = ' '.join(text)
        date1 = text[:12]
        date2 = text[-13:]
        return date1, date2
    else :
        date = [
            convert_datetime_string_to_isoformat_datetime(i[:-5].replace(' ', '')) \
            for i \
            in text.split(' ~ ')
        ]
        return date[0], date[1]