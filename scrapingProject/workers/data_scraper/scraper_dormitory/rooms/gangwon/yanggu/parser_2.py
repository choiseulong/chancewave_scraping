from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_title', 'extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-02-09 
    header = ["교육구분", "분류", "강좌명", "강사명", "인원", "대상", "교육시간", "교육장소", "강의계획서", "수강신청"]
    tbody = extract_children_tag(soup, 'tbody', is_child_multiple=True)
    if type(tbody) == type(None):
        return
    else :
        tbody = tbody[1]
    cont_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for cont in cont_list :
        td_list = extract_children_tag(cont, 'td', is_child_multiple=True)
        extra_info = {'info_title':'강좌정보'}
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            extra_info.update({f'info_{len(extra_info)}' : (header[td_idx], td_text)})
            if header[td_idx] == '강좌명':
                var['post_title'].append(td_text)
        var['extra_info'].append([extra_info])
    result = merge_var_to_dict(key_list, var)
    return result
