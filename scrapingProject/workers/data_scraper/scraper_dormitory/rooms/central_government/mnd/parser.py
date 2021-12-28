from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'uploader', 'view_count']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)

    contents = extract_children_tag(soup, 'ul', {'class' : 'list_post'}, DataStatus.not_multiple)
    liList = extract_children_tag(contents, 'li', DataStatus.empty_attrs, DataStatus.multiple)
    if not liList :
        return
    for li in liList :
        a_tag = extract_children_tag(li, 'a', {'title' : True}, DataStatus.not_multiple)
        postId = extract_text_between_prefix_and_suffix(
            'boardSeq=',
            '&amp',
            extract_attrs(
                a_tag,
                'href'
            )
        )
        var['post_url'].append(
            var['post_url_frame'].format(postId)
        )
        var['post_title'].append(
            extract_text(a_tag)
        )
        postInfoList = extract_children_tag(li, 'div', {'class' : 'post_info'}, DataStatus.multiple)
        for infoIdx, postInfo in enumerate(postInfoList):
            infoText = extract_text(postInfo).split(':')[-1].strip()
            if infoIdx == 0 :
                var['uploader'].append(infoText)
            elif infoIdx == 1 :
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(infoText)
                )
            elif infoIdx == 2 :
                var['view_count'].append(
                    extract_numbers_in_text(infoText)
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
    var, soup, key_list, fullText = html_type_default_setting(params, target_key_info)
    if type(soup) == str :
        # ERROR 예외 : [local variable 'match' referenced before assignment] bug
        # UserWarning: unknown status keyword 'data-hwpjson' in marked section warnings.warn(msg)
        fullText = fullText.replace('[data-hwpjson]', '')
        soup = change_to_soup(fullText)

    post_content = extract_children_tag(soup, 'div', {'class' : 'post_content'}, DataStatus.not_multiple)
    post_text = extract_text(post_content)
    var['contact'] = extract_contact_numbers_from_text(post_text)
    var['post_text'] = clean_text(post_text)
    var['post_image_url'] = search_img_list_in_contents(post_content, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    return result
