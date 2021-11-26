from workers.dataScraper.scraperDormitory.parserTools.tools import *

childIsMultiple = True
childIsNotMultiple = False
dummpyAttrs = {}

def postListParsingProcess(**params):
    targetKeyInfo = {
        'listType' : ['postSubject', 'postTitle', 'uploadedTime', 'startDate', 'endDate', 'viewCount'],
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
                extract_children_tag(board_body, 'a', dummpyAttrs, childIsNotMultiple)
            )
        )
        dateList = extract_children_tag(board_body, 'div', {"class" : "date"}, childIsMultiple)
        if len(dateList) == 2 :
            var['uploadedTime'].append(
                convert_datetime_string_to_isoformat_datetime(dateList[0])
            )
            ongoingDateRange = dateList[1].split(' ~ ')
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
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    print(result)
    # return result



def postContentParsingProcess(**params):
    targetKeyInfo = {
        'listType' : ['extraInfo', 'postImageUrl', 'linkedPostUrl'],
        'strType' : ['postContentTarget', 'contact', 'postTextType']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)



    
    # tender_con_list = extract_text(soup, 'div', {"class" : "tender_con"}, childIsMultiple)
    # for tender_con in tender_con_list :
    #     title = extract_text(extract_children_tag(tender_con, 'h4', dummpyAttrs, childIsNotMultiple))
    #     if title == '문의처':
    #         pass