from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    ulBox = extract_children_tag(soup, 'ul', {'class' : 'lst1'}, is_child_multiple=False)
    liList = extract_children_tag(ulBox, 'li', child_tag_attrs={}, is_child_multiple=True)
    if not liList :
        return 
    for li in liList:
        post_thumbnail = extract_children_tag(li, 'img')
        if post_thumbnail:
            src = extract_attrs(post_thumbnail, 'src')
            if 'image.do?' in src:
                var['post_thumbnail'].append(
                    var['channel_main_url'] + src
                )
            else :
                var['post_thumbnail'].append('')
        else :
            var['post_thumbnail'].append('')
        a_tag = extract_children_tag(li, 'a', {'class' : 'a1'}, is_child_multiple=False)
        href = extract_attrs(a_tag, 'href')
        postId = extract_text_between_prefix_and_suffix('&idx=', '&amode', href)
        var['post_url'].append(
            var['post_url_frame'].format(postId)
        )
        strong = extract_children_tag(li, 'strong', {'class' :'t1'}, is_child_multiple=False)
        var['post_title'].append(
            extract_text(strong)
        )
        wrap1t3 = extract_children_tag(li, 'i', {'class' : 'wrap1t3'}, is_child_multiple=False)
        spanList = extract_children_tag(wrap1t3, 'span', child_tag_attrs={}, is_child_multiple=True)
        for spanIdx, span in enumerate(spanList):
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

    
    result = merge_var_to_dict(key_list, var)
    
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
    
    result = convert_merged_list_to_dict(key_list, var)
    
    return result
