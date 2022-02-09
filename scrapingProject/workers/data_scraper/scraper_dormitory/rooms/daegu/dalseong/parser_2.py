from pickle import FALSE
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_title', 'post_url', 'is_going_on', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    lec_list = extract_children_tag(soup, 'tr', child_tag_attrs={'class':'tac'}, is_child_multiple=True)
    if type(lec_list) == None:
        return
    for lec in lec_list :
        td_list = extract_children_tag(lec, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 0 :
                var['post_subject'].append(
                    td_text
                )
            elif td_idx == 1:
                a_tag = extract_children_tag(td, 'a')
                href = extract_attrs(a_tag ,'href')
                post_id = parse_post_id(href, 0)
                var['post_url'].append(
                    var['post_url_frame'] + post_id
                )
                var['post_title'].append(
                    td_text
                )
            elif td_idx == 5 :
                if '마감' in td_text:
                    var['is_going_on'].append(False)
                else :
                    print(var['channel_code'], 'is_going_on 확인 필요')
                    var['is_going_on'].append(True)
    result = merge_var_to_dict(key_list, var)
    # 2021-02-04 header ["분류", "교육과정", "수강료", "접수기간/교유기간", "접수인원", "진행상황"]
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'start_date', 'end_date', 'post_text_type', 'start_date2', 'end_date2'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    extra_info = {'info_title' : '교육 및 강좌 상세'}
    var['post_text_type'] = 'only_extra_info'
    table = extract_children_tag(soup, 'table')
    tmp_meta_data = extract_children_tag(table, 'th', is_child_multiple=True)
    for meta_data in tmp_meta_data:
        meta_data_name = extract_text(meta_data)
        meta_data_value = extract_text(find_next_tag(meta_data))
        extra_info.update({f'info_{len(extra_info)}' : (meta_data_name, meta_data_value)})
        if '문의전화' in meta_data_name:
            var['contact'] = meta_data_value
        elif '대상' in meta_data_name :
            var['post_content_target'] = meta_data_value
        elif '접수기간' in meta_data_name:
            var['start_date'], var['end_date'] = parse_date_text(meta_data_value)
        elif '교육기간' in meta_data_name:
            var['start_date2'], var['end_date2'] = parse_date_text(meta_data_value)
    var['extra_info'].append(extra_info)
    result = convert_merged_list_to_dict(key_list, var)
    return result

def parse_date_text(text):
    text_split = text.split(' ~ ')
    if len(text_split) == 2:
        result = [convert_datetime_string_to_isoformat_datetime(_[:10]) for _ in text_split]
        return result[0], result[1]
    else :
        return None, None
