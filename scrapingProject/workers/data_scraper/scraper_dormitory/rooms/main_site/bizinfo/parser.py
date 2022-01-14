from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'start_date', 'end_date', 'uploader', 'uploaded_time', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=False)
    contents_tr = extract_children_tag(tbody, 'tr', child_tag_attrs={}, is_child_multiple=True)
    for tr in contents_tr :
        anchor = extract_children_tag(tr, 'a', child_tag_attrs={}, is_child_multiple=False)
        var['post_url'].append(
            var['post_url_frame'].format(
                    extract_params(
                       extract_attrs(anchor, 'onclick')
                )
            )
        )
        var['post_title'].append(
            extract_text(anchor)
        )
        contents_td = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True)
        for idx, td in enumerate(contents_td):
            td_text = extract_text(td)
            if idx == 2:
                if '~' in td_text:
                    date = td_text.split(' ~ ')
                    date = [convert_datetime_string_to_isoformat_datetime(date[0]), convert_datetime_string_to_isoformat_datetime(date[1])]
                else :
                    date = [td_text, td_text]
                var['start_date'].append(
                    date[0]
                )
                var['end_date'].append(
                    date[1]
                )
            elif idx == 3:
                var['uploader'].append(td_text)
            elif idx == 4:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif idx == 5:
                var['view_count'].append(extract_numbers_in_text((td_text)))

    
    result = merge_var_to_dict(key_list, var)
    return result

def extract_params(text):
    prefix = "('"
    suffix = "')"
    return text[text.find(prefix)+len(prefix):text.find(suffix)]

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_subject', 'post_text_type'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text_type'] = 'only_extra_info'
    tbody_list = extract_children_tag(soup, 'tbody', child_tag_attrs={}, is_child_multiple=True)
    tr = extract_children_tag(tbody_list[0], 'tr', child_tag_attrs={}, is_child_multiple=False) 
    td_list = extract_children_tag(tr, 'td', child_tag_attrs={}, is_child_multiple=True) 
    var['post_subject'] = extract_text(td_list[0])

    boardBusiness = extract_children_tag(soup, 'div', {"class" : "boardBusiness"}, is_child_multiple=False)
    h4_contName = extract_children_tag(boardBusiness, 'h4', {"class" : True}, is_child_multiple=True)
    extraDict = {"info_title" : "지원사업 상세"}

    for h4 in h4_contName:
        h4_text = extract_text(h4)
        next_tag = find_next_tag(h4)
        next_tag_class_attrs = extract_attrs(next_tag, 'class')[0]
        if next_tag_class_attrs == "contBox":
            next_tag_text = clean_text(extract_text(next_tag))
            extraInfoLength = len(extraDict)
            extraDict.update({f'info_{extraInfoLength}' : [h4_text, next_tag_text]})
    
    var['extra_info'].append(extraDict)
    
    result = convert_merged_list_to_dict(key_list, var)
    return result



    