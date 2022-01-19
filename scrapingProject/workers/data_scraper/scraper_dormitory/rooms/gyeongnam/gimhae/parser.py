from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader', 'post_subject']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    liList = extract_children_tag(soup, 'li', {'class' : 'li1'}, is_child_multiple=True)
    if not liList:
        return
    for li in liList:
        em = extract_children_tag(li, 'em', child_tag_attrs={}, is_child_multiple=False)
        if em:
            post_subject = extract_text(em)[1:-1]
        else :
            post_subject = ''
        var['post_subject'].append(post_subject)
        strong = extract_children_tag(li, 'strong', child_tag_attrs={}, is_child_multiple=False)
        post_title = extract_text(strong).replace('새 글', '').replace(post_subject, '').strip()
        var['post_title'].append(post_title)
        spanList = extract_children_tag(li, 'span', {'class' : 't3'}, is_child_multiple=True)
        uploader = ''
        for spanIdx, span in enumerate(spanList):
            spanText = extract_text(span)
            if spanIdx == 0:
                var['uploaded_time'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        spanText
                    )
                )
            elif spanIdx in [1, 2] :
                uploader += spanText + ' '
            elif spanIdx == 3 :
                var['view_count'].append(
                    extract_numbers_in_text(spanText)
                )
        var['uploader'].append(uploader)
        a_tag = extract_children_tag(li, 'a', child_tag_attrs={}, is_child_multiple=False)
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
            

    
    result = merge_var_to_dict(key_list, var)
    # print(result)
    return result

def post_content_parsing_process(**params):
    target_key_info = {
        'single_type' : ['contact', 'post_text'],
        'multiple_type' : ['post_image_url']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    info1 = extract_children_tag(soup, 'div', {'class' : 'info1'}, is_child_multiple=False)
    dtList = extract_children_tag(info1, 'dt', child_tag_attrs={}, is_child_multiple=True)
    for dt in dtList:
        dtText = extract_text(dt)
        if '전화번호' in dtText:
            var['contact'] = extract_contact_numbers_from_text(
                dtText
            )
            break

    substance = extract_children_tag(soup, 'div', {'class' : 'substance'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(substance))
    var['post_image_url'] = search_img_list_in_contents(substance, var['channel_main_url'])
    # 이미지 요청시 Referer을 header에 담아 보내야함 
    # Referer = post_url
    
    result = convert_merged_list_to_dict(key_list, var)
    # print(result)
    return result


