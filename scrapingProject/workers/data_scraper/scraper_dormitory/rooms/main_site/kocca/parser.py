from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postSubject', 'postTitle', 'uploadedTime', 'startDate', 
        'endDate', 'viewCount', 'postUrl'],
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    board_list_body = extract_children_tag(soup, 'div', {"class" : "body_row"}, childIsMultiple)
    for board_body in board_list_body:
        var['postSubject'].append(
            extract_text(
                extract_children_tag(board_body, 'p', {"class" : "pimsBtn"}, childIsNotMultiple)
            )
        )
        var['postTitle'].append(
            extract_text(
                extract_children_tag(board_body, 'a', dummyAttrs, childIsNotMultiple)
            )
        )
        dateList = extract_children_tag(board_body, 'div', {"class" : "date"}, childIsMultiple)
        dateText = [extract_text(date) for date in dateList]

        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(dateText[1])
        )
        ongoingDateRange = dateText[2].split(' ~ ')
        var['startDate'].append(
            convert_datetime_string_to_isoformat_datetime(ongoingDateRange[0])
        )
        var['endDate'].append(
            convert_datetime_string_to_isoformat_datetime(ongoingDateRange[1])
        )
        var['viewCount'].append(
            extract_numbers_in_text (
                extract_text(
                    extract_children_tag(board_body, 'div', {'class' : 'hit'})
                )
            )
        )
        url = extract_attrs(
            extract_children_tag(board_body, 'a', dummyAttrs, childIsNotMultiple),
            'href'
        ) 
        var['postUrl'].append(
            var['channelMainUrl'] + url
        )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    print(result)
    # return result



def postContentParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['extraInfo'],
        'singleType' : ['postTextType', 'postText', 'contact']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    var['postTextType'] = 'both'

    extraDict = {'infoTitle' : '지원사업 상세'}
    tender_con_list = extract_children_tag(soup, 'div', {"class" : "tender_con"}, childIsMultiple)
    for tender_con in tender_con_list :
        title = extract_text(extract_children_tag(tender_con, 'h4', dummyAttrs, childIsNotMultiple))
        tableData = clean_text(
            extract_text(extract_children_tag(tender_con, 'td', dummyAttrs, childIsNotMultiple))
        )
        if title in ['사업개요', '지원내용']:
            var['postText'] += tableData + '\n'
        elif title == '문의처': 
            var['contact'] = tableData
        lenExtraInfo = len(extraDict)
        extraDict.update({f'info_{lenExtraInfo}' : [title, tableData]})
    var['extraInfo'].append(extraDict)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
