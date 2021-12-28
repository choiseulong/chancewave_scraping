from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_subject', 'post_title', 'uploaded_time', 'start_date', 
        'end_date', 'view_count', 'post_url'],
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    board_list_body = extract_children_tag(soup, 'div', {"class" : "body_row"}, DataStatus.multiple)
    for board_body in board_list_body:
        var['post_subject'].append(
            extract_text(
                extract_children_tag(board_body, 'p', {"class" : "pimsBtn"}, DataStatus.not_multiple)
            )
        )
        var['post_title'].append(
            extract_text(
                extract_children_tag(board_body, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
            )
        )
        dateList = extract_children_tag(board_body, 'div', {"class" : "date"}, DataStatus.multiple)
        dateText = [extract_text(date) for date in dateList]

        var['uploaded_time'].append(
            convert_datetime_string_to_isoformat_datetime(dateText[1])
        )
        ongoingDateRange = dateText[2].split(' ~ ')
        var['start_date'].append(
            convert_datetime_string_to_isoformat_datetime(ongoingDateRange[0])
        )
        var['end_date'].append(
            convert_datetime_string_to_isoformat_datetime(ongoingDateRange[1])
        )
        var['view_count'].append(
            extract_numbers_in_text (
                extract_text(
                    extract_children_tag(board_body, 'div', {'class' : 'hit'})
                )
            )
        )
        url = extract_attrs(
            extract_children_tag(board_body, 'a', DataStatus.empty_attrs, DataStatus.not_multiple),
            'href'
        ) 
        var['post_url'].append(
            var['channel_main_url'] + url
        )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result



def post_content_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['extra_info'],
        'single_type' : ['post_text_type', 'post_text', 'contact']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'both'

    extraDict = {'info_title' : '지원사업 상세'}
    tender_con_list = extract_children_tag(soup, 'div', {"class" : "tender_con"}, DataStatus.multiple)
    for tender_con in tender_con_list :
        title = extract_text(extract_children_tag(tender_con, 'h4', DataStatus.empty_attrs, DataStatus.not_multiple))
        tableData = clean_text(
            extract_text(extract_children_tag(tender_con, 'td', DataStatus.empty_attrs, DataStatus.not_multiple))
        )
        if title in ['사업개요', '지원내용']:
            var['post_text'] += tableData + '\n'
        elif title == '문의처': 
            var['contact'] = tableData
        lenExtraInfo = len(extraDict)
        extraDict.update({f'info_{lenExtraInfo}' : [title, tableData]})
    var['extra_info'].append(extraDict)

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
