from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    contentsList = extract_children_tag(soup, 'div', {'class' : 'toggle'}, DataStatus.multiple)
    for contents in contentsList:
        a_tag = extract_children_tag(contents, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
        postId = extract_numbers_in_text(
            extract_attrs(a_tag, 'onclick')
        )
        var['post_url'].append(
            var['post_url_frame'].format(postId)
        )
    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text', 'uploader', 'uploaded_time', 'post_title'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    view_head = extract_children_tag(soup, 'div', {'class' : 'view_head'}, DataStatus.not_multiple)
    spanList = extract_children_tag(view_head, 'span', {'class' : True}, DataStatus.multiple)
    var['post_title'] = extract_text(
        extract_children_tag(view_head, 'h2', DataStatus.empty_attrs, DataStatus.not_multiple)
    )
    for span in spanList:
        spanText = extract_text(span)
        if '부서' in spanText or '담당자' in spanText:
            var['uploader'] += extract_text(find_next_tag(span)) + ' '
        elif '연락처' in spanText:
            var['contact'] = extract_contact_numbers_from_text(extract_text(find_next_tag(span)))
        elif '작성일' in spanText:
            var['uploaded_time'] = convert_datetime_string_to_isoformat_datetime(
                    extract_text(find_next_tag(span))
                )
            
    contBox = extract_children_tag(soup, 'div', {'id' : 'cont-wrap'}, DataStatus.not_multiple)
    var['post_text'] = clean_text(extract_text(contBox))
    var['post_image_url'] = search_img_list_in_contents(contBox, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result