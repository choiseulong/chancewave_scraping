from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['view_count', 'post_title', 'uploader', 'uploaded_time', 'contents_req_params']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    tbody = extract_children_tag(soup, 'tbody', DataStatus.empty_attrs, DataStatus.multiple)
    if len(tbody):
        tbody = tbody[1]
    else :
        return
    contentsBox = extract_children_tag(tbody, 'tr', DataStatus.empty_attrs, DataStatus.multiple)
    for contents in contentsBox:
        td_list = extract_children_tag(contents, 'td', DataStatus.empty_attrs, DataStatus.multiple)
        for td_idx, td in enumerate(td_list):
            td_text = extract_text(td)
            if td_idx == 1:
                var['post_title'].append(td_text) 
                nttId = parse_href(
                    extract_attrs(
                        extract_children_tag(td, 'a', DataStatus.empty_attrs, DataStatus.not_multiple),
                        'onclick'
                    )
                )
                data = {
                    "bbsId" : "BBSMSTR_000000002424",
                    "bbsTyCode" : "BBST01",
                    "nttId" : nttId,
                    "pageIndex" : 1
                }
                var['contents_req_params'].append(
                    data
                )
            elif td_idx == 2:
                var['uploader'].append(td_text)
            elif td_idx == 3:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        td_text
                    )
                )
            elif td_idx == 5 :
                var['view_count'].append(
                    extract_numbers_in_text(td_text)
                )
            else :
                continue

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def parse_href(text):
    prefix = "('"
    suffix = "')"
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result

    
def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['post_text'],
        'multiple_type' : ['post_image_url', 'contact']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    contents = extract_children_tag(soup, 'td', {'class' : 'bbs_content'}, DataStatus.not_multiple)
    post_text = extract_text(contents)
    if post_text:
        var['post_text'] = clean_text(post_text)
        var['contact'] = extract_contact_numbers_from_text(post_text)
    img_list = extract_children_tag(contents, 'img', DataStatus.empty_attrs, DataStatus.multiple)
    if img_list :
        for img in img_list:
            href = extract_attrs(img, 'href')
            if 'http' not in href:
                href = var['channel_main_url'] + href
            var['post_image_url'].append(href)

    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
