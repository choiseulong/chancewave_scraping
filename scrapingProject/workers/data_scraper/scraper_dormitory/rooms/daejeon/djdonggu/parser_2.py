from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'is_going_on']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    for key in key_list :
        var[f'parse_{key}'] = globals()[f'parse_{key}']
    # 2021-01-19
    thead = extract_children_tag(soup, 'thead', is_child_multiple=True)[1]
    var['table_header_box'] = extract_children_tag(thead, 'tr')
    var['post_id_idx'] = [1,2]
    var['table_header'] = ["번호", "강좌명", "모집기간", "운영기간", "신청/모집", "수강료", "접수상태"]
    result = parse_board_type_html_page(soup, var, key_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'start_date', 'end_date'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody')
    th_list = extract_children_tag(tbody, 'th', is_child_multiple=True)
    extra_info = {'info_title':'강의정보'}
    for th in th_list :
        th_text = extract_text(th)
        td_text = extract_text(find_next_tag(th))
        extra_info.update({f'info_{len(extra_info)}' : (th_text, td_text)})
        if '문의전화' in th_text:
            var['contact'] = td_text
        elif '수강신청기간' in th_text :
            td_text_split = td_text.split('~')
            if td_text_split :
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(
                    td_text_split[0].strip()
                )
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(
                    td_text_split[1].strip()
                )
            else :
                var['start_date'] = convert_datetime_string_to_isoformat_datetime(
                    None
                )
                var['end_date'] = convert_datetime_string_to_isoformat_datetime(
                    None
                )
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    return result

