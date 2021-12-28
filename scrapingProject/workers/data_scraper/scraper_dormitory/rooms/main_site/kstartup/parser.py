from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_subject', 'post_title', 'contents_req_params', 'view_count', 'uploader', 'end_date']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    CSRF_NONCE = extract_attrs(
        extract_children_tag(soup, 'input', {"name" : "CSRF_NONCE"}, DataStatus.not_multiple),
        'value'
    )
    tagList = [
        i \
        for i \
        in extract_children_tag(soup, 'li', {'id' : True, 'style' : True, 'class':False}, DataStatus.multiple)
        if 'liArea' in extract_attrs(i, 'id')
    ]
    for tag in tagList :
        spanList = extract_children_tag(tag, 'span', {"class" : True}, DataStatus.multiple)
        for span in spanList :
            if 'ann_list_group' in extract_attrs(span, 'class')[0]:
                var['post_subject'].append(extract_text(span))
    var['post_title'] = [
        extract_text(
            extract_children_tag(tag, 'a')
        ) \
        for tag \
        in tagList
    ]

    for tag in tagList :
        tag = extract_children_tag(tag, 'a', {'style' : True, 'title' : True})
        href = extract_attrs(tag, 'href')
        prefix_length = href.find('(')
        tuple_result = convert_text_to_tuple(href[prefix_length:])
        reqParams = {
            "CSRF_NONCE" : CSRF_NONCE,
            "mid" : 30004,
            "searchPrefixCode" : tuple_result[0],
            "searchPostSn" : tuple_result[1]
        }
        var['contents_req_params'].append(reqParams)

    infoIdxRoot = {1:'uploader', 2:'end_date', 3:'view_count'}
    for tag in tagList:
        ann_list_info = extract_children_tag(tag, 'ul', {"class" : "ann_list_info"})
        ann_list_info_li = extract_children_tag(ann_list_info, 'li', DataStatus.empty_attrs, DataStatus.multiple)

        for infoIdx in range(len(ann_list_info_li)) :
            if infoIdx in infoIdxRoot.keys():
                text = extract_text(ann_list_info_li[infoIdx])
                if infoIdx == 3 :
                    text = extract_numbers_in_text(text)
                elif infoIdx == 2 :
                    text = convert_datetime_string_to_isoformat_datetime(text[5:])
                var[infoIdxRoot[infoIdx]].append(
                    text
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact', 'post_content_target', 'post_text_type'],
        'multiple_type' : ['extra_info']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    var['post_text'] = clean_text(
        extract_attrs(
            extract_children_tag(soup, 'meta', {'name' : 'og:description'}, DataStatus.not_multiple),
            'content'
        ) 
    )
    extraDict = {"info_title" : "공고 개요"}
    table = extract_children_tag(soup, 'table', {"class" : ["tbl_gray", "mgb_10"]}, DataStatus.not_multiple)
    
    th = extract_children_tag(table, 'th', DataStatus.empty_attrs, DataStatus.multiple)
    td = extract_children_tag(table, 'td', DataStatus.empty_attrs, DataStatus.multiple)
    for infoName, infoValue in zip(th, td):
        infoName = extract_text(infoName)
        infoValue = extract_text(infoValue)

        if infoName == '대상': 
            var['post_content_target'] += "대상:" + infoValue + ' - '
        elif infoName == '대상연령': 
            var['post_content_target'] += "대상연령:" + infoValue
        elif infoName in ['담당부서', '연락처']:
            var['contact'] += infoValue + ' '
        else :
            extra_info = [infoName, infoValue]
            extraDict.update({f'info_{len(extraDict)}' : extra_info})
    var['extra_info'].append(extraDict)
    var['post_text_type'] = 'both'
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result 
