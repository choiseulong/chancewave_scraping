from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'post_url', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'text_center'}, DataStatus.not_multiple)
    tr_list = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for tr in tr_list:
        td_list = extract_children_tag(tr, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                href = extract_attrs(
                    extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple),
                    'href'
                )
                if 'html' not in href :
                    href = parse_href(href)
                    href = var['post_url_frame'].format(href)
                var['post_url'].append(href)
                var['post_title'].append(td_text.replace('새글', ''))
            elif td_idx == 3 :
                var['uploader'].append(td_text)
            elif td_idx == 4:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif td_idx == 5 :
                var['view_count'].append(extract_numbers_in_text(td_text))

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def parse_href(text):
    prefix = 'nttNo='
    suffix = '&searchCtgry'
    return text[text.find(prefix) + len(prefix) : text.find(suffix)]
    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'p-table--th-left'}, DataStatus.not_multiple)
    thList = extract_children_tag(tbody, 'th', DataStatus.empty_attrs, DataStatus.multiple)
    tdCount = 0
    for th in thList :
        td_text = extract_text(th)
        if td_text in ['부서', '연락처'] :
            nextTh = find_next_tag(th)
            nextThText = extract_text(nextTh)
            var['contact'] += nextThText + ' '
            tdCount += 1
        if tdCount == 2 :
            break
    content = extract_children_tag(tbody, 'td', {'class' : 'p-table__content'}, DataStatus.not_multiple)
    var['post_text'] = extract_text(content)
    
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
    