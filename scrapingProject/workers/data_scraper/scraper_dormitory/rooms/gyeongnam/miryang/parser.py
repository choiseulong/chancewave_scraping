from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    liList = extract_children_tag(soup, 'li', {'class' : 'Lst-Li'}, DataStatus.multiple)
    if not liList:
        return
    for li in liList:
        a_tag = extract_children_tag(li, 'a', DataStatus.empty_attrs, DataStatus.not_multiple)
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['channel_main_url'] + href
        )
        post_subject = extract_text(
                extract_children_tag(li, 'em', DataStatus.empty_attrs, DataStatus.not_multiple)
            )
        if post_subject:
            var['post_subject'].append(post_subject[1:-1])
        else :
            var['post_subject'].append(None)
        post_title = extract_text(
                extract_children_tag(li, 'strong', DataStatus.empty_attrs, DataStatus.not_multiple)
            )
        var['post_title'].append(
            post_title.replace(post_subject, '')
        )
        infoBox = extract_children_tag(li, 'span', {'class' : 'Lit-DateBx'}, DataStatus.not_multiple)
        spanList = extract_children_tag(infoBox, 'span', DataStatus.empty_attrs, DataStatus.multiple)
        for spanIdx, span in enumerate(spanList) :
            spanText = extract_text(span)
            if spanIdx == 0 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(spanText)
                )
            elif spanIdx == 1 :
                var['uploader'].append(spanText)
            elif spanIdx == 2 :
                var['view_count'].append(
                    extract_numbers_in_text(spanText)
                )

    value_list = [var[key] for key in key_list]
    result = merge_var_to_dict(key_list, value_list)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    cont = extract_children_tag(soup, 'div', {'class' : 'cont'}, DataStatus.not_multiple)
    post_text = extract_text(cont)
    var['post_text'] = clean_text(post_text)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(cont, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result
