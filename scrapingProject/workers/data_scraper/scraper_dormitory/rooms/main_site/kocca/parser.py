from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_subject', 'post_title', 'uploaded_time', 'start_date', 
        'end_date', 'view_count', 'post_url'],
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', is_child_multiple=False)
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for tr in tr_list :
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 :
                var['post_subject'].append(td_text)
            elif td_idx == 1 :
                var['post_title'].append(td_text)
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag, 'href')
                var['post_url'].append(var['channel_main_url'] + href)
            elif td_idx == 2:
                var['uploaded_time'].append(convert_datetime_string_to_isoformat_datetime(td_text))
            elif td_idx == 3 :
                var['start_date'].append(convert_datetime_string_to_isoformat_datetime(td_text.split('~')[0].strip()))
                var['end_date'].append(convert_datetime_string_to_isoformat_datetime(td_text.split('~')[1].strip()))
            elif td_idx == 4 :
                var['view_count'].append(td_text)

    # board_list_body = extract_children_tag(soup, 'div', {"class" : "body_row"}, is_child_multiple=True)
    # for board_body in board_list_body:
    #     var['post_subject'].append(
    #         extract_text(
    #             extract_children_tag(board_body, 'p', {"class" : "pimsBtn"}, is_child_multiple=False)
    #         )
    #     )
    #     var['post_title'].append(
    #         extract_text(
    #             extract_children_tag(board_body, 'a', child_tag_attrs={}, is_child_multiple=False)
    #         )
    #     )
    #     dateList = extract_children_tag(board_body, 'div', {"class" : "date"}, is_child_multiple=True)
    #     dateText = [extract_text(date) for date in dateList]

    #     var['uploaded_time'].append(
    #         convert_datetime_string_to_isoformat_datetime(dateText[1])
    #     )
    #     ongoingDateRange = dateText[2].split(' ~ ')
    #     var['start_date'].append(
    #         convert_datetime_string_to_isoformat_datetime(ongoingDateRange[0])
    #     )
    #     var['end_date'].append(
    #         convert_datetime_string_to_isoformat_datetime(ongoingDateRange[1])
    #     )
    #     var['view_count'].append(
    #         extract_numbers_in_text (
    #             extract_text(
    #                 extract_children_tag(board_body, 'div', {'class' : 'hit'})
    #             )
    #         )
    #     )
    #     url = extract_attrs(
    #         extract_children_tag(board_body, 'a', child_tag_attrs={}, is_child_multiple=False),
    #         'href'
    #     ) 
    #     var['post_url'].append(
    #         var['channel_main_url'] + url
    #     )
    
    result = merge_var_to_dict(key_list, var)
    return result



def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    board_cont = extract_children_tag(soup, 'div', child_tag_attrs={"class" : "board_cont"}, is_child_multiple=False)
    var['post_text'] = extract_text(board_cont)

    # extraDict = {'info_title' : '지원사업 상세'}
    # tender_con_list = extract_children_tag(soup, 'div', {"class" : "tender_con"}, is_child_multiple=True)
    # for tender_con in tender_con_list :
    #     title = extract_text(extract_children_tag(tender_con, 'h4', child_tag_attrs={}, is_child_multiple=False))
    #     tableData = clean_text(
    #         extract_text(extract_children_tag(tender_con, 'td', child_tag_attrs={}, is_child_multiple=False))
    #     )
    #     if title in ['사업개요', '지원내용']:
    #         var['post_text'] += tableData + '\n'
    #     elif title == '문의처': 
    #         var['contact'] = tableData
    #     lenExtraInfo = len(extraDict)
    #     extraDict.update({f'info_{lenExtraInfo}' : [title, tableData]})
    # var['extra_info'].append(extraDict)

    
    result = convert_merged_list_to_dict(key_list, var)
    return result
