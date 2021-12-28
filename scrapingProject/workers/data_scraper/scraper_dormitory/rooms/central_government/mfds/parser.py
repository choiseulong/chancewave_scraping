from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'post_url', 'uploaded_time']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    mainDiv = extract_children_tag(soup, 'div', {'class' : 'bbs_list01'}, DataStatus.not_multiple)
    if '0' in var['channel_code']:
        ulList = extract_children_tag(mainDiv, 'ul', DataStatus.empty_attrs, DataStatus.multiple, DataStatus.not_recursive)
        if len(ulList):
            ulList = ulList[1]
    else :
        ulList = extract_children_tag(mainDiv, 'ul', DataStatus.empty_attrs, DataStatus.not_multiple)

    if not ulList :
        return
    var['uploaded_time'] = [
        convert_datetime_string_to_isoformat_datetime(
            extract_text(i)
        )
        for i \
        in extract_children_tag(ulList, 'div', {'class' : 'right_column'}, DataStatus.multiple)
    ]
    aTagList = [
        a_tag for a_tag in extract_children_tag(ulList, 'a', DataStatus.empty_attrs, DataStatus.multiple) \
        if 'title' in extract_attrs(a_tag, 'class')
    ]
    for a_tag in aTagList:
        href = extract_attrs(a_tag, 'href')
        if 'html' not in href:
            href = parse_href(href)
            href = var['post_url_frame'].format(href)
        var['post_url'].append(href)
        var['post_title'].append(extract_text(a_tag))

    winfoList = extract_children_tag(ulList, 'div', {"class" : "winfo"}, DataStatus.multiple)
    for winfo in winfoList:
        pTagList = extract_children_tag(winfo, 'p', DataStatus.empty_attrs, DataStatus.multiple)
        for pTag in pTagList:
            pText = extract_text(pTag)
            if '담당부서' in pText:
                var['uploader'].append(pText.split(' | ')[1])
            elif '조회수' in pText:
                var['view_count'].append(
                    extract_numbers_in_text(pText)
                )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def parse_href(text):
    prefix = 'seq='
    suffix = '&amp'
    return text[text.find(prefix) + len(prefix) : text.find(suffix)]
    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text', 'contact'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contentBox = extract_children_tag(soup, 'div', {'class' : 'bv_cont'}, DataStatus.not_multiple)
    contactBox = extract_children_tag(soup, 'div', {'class' : 'bbs_sat_header'}, DataStatus.not_multiple)
    if contactBox:
        spanList = extract_children_tag(contactBox, 'span', DataStatus.empty_attrs, DataStatus.multiple)
        if spanList:
            for span in spanList:
                spanText = extract_text(span)
                var['contact'] += spanText + ' '
    var['post_text'] = extract_text(contentBox)
    imgBox = extract_children_tag(contentBox, 'img', DataStatus.empty_attrs, DataStatus.multiple)
    if imgBox:
        for img in imgBox:
            src = extract_attrs(img,'src')
            if 'html' not in src:
                src = var['channel_main_url'] + src
            var['post_image_url'].append(src)
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result