from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['extra_info', 'post_title', 'post_content_target']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    # 2021-01-24 header ["카테고리", "프로그램명", "요일", "수강시간", "장소", "정원", "대상", "수강료", "접수방법"]
    thead = extract_children_tag(soup, 'thead')
    header_list = [header.text for header in extract_children_tag(thead, 'th', is_child_multiple=True)]
    tbody = extract_children_tag(soup, 'tbody')
    tr_list = extract_children_tag(tbody, 'tr', is_child_multiple=True)
    for tr in tr_list:
        extra_info = {'info_title':'프로그램상세'}
        td_list = extract_children_tag(tr, 'td', is_child_multiple=True)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            extra_info.update({f'info_{len(extra_info)}' : (header_list[td_idx], td_text)})
            if td_idx == 1 :
                var['post_title'].append(td_text)
            elif td_idx == 6 :
                var['post_content_target'].append(td_text)
        var['extra_info'].append(extra_info)
    result = merge_var_to_dict(key_list, var)
    return result