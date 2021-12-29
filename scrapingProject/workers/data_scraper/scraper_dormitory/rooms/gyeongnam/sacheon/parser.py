from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def post_list_parsing_process(**params):
    target_key_info = {
        'multiple_type' : ['post_url', 'post_title', 'uploaded_time', 'view_count', 'uploader', 'post_thumbnail']
    }
    var, soup, key_list, _ = html_type_default_setting(params, target_key_info)
    ulBox = extract_children_tag(soup, 'ul', {'class' : 'lst1'}, is_child_multiple=False)
    liList = extract_children_tag(ulBox, 'li', child_tag_attrs={}, is_child_multiple=True)
    if not liList:
        return
    for li in liList:
        a_tag = extract_children_tag(li, 'a', child_tag_attrs={}, is_child_multiple=False)
        href = extract_attrs(a_tag, 'href')
        var['post_url'].append(
            var['post_url_frame'] + href
        )
        spanF1 = extract_children_tag(li, 'span', {'class' : 'f1'}, is_child_multiple=False)
        if spanF1:
            img = extract_children_tag(spanF1, 'img', child_tag_attrs={}, is_child_multiple=False)
            src = extract_attrs(img, 'src')
            var['post_thumbnail'].append(
                var['channel_main_url'] + src
            )
        else :
            var['post_thumbnail'].append(
                None
            )
        var['post_title'].append(
            extract_text(
                extract_children_tag(li, 'strong', {"class" : "t1"}, is_child_multiple=False)
            )
        )
        wrap1t3 = extract_children_tag(li, 'i', {'class':'wrap1t3'}, is_child_multiple=False)
        spanList = extract_children_tag(wrap1t3, 'span', child_tag_attrs={}, is_child_multiple=True)
        for spanIdx, span in enumerate(spanList):
            spanText = extract_text(span)
            if spanIdx == 0:
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
    result = merge_var_to_dict(key_list, value_list, var['channel_code'])
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
    for dt in dtList :
        dtText = extract_text(dt)
        if '연락처' in dtText:
            var['contact'] = dtText.split(':')[1].strip()
            break
    substance = extract_children_tag(soup, 'div', {'class' : 'substance'}, is_child_multiple=False)
    var['post_text'] = clean_text(extract_text(substance))
    var['post_image_url'] = search_img_list_in_contents(substance, var['channel_main_url'])
    value_list = [var[key] for key in key_list]
    result = convert_merged_list_to_dict(key_list, value_list)
    # print(result)
    return result
