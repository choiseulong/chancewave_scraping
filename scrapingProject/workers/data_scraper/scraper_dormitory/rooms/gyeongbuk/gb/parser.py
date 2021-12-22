from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = extract_text_between_prefix_and_suffix('&B_NUM=', '&B_STEP', href)
                B_STEP = extract_text_between_prefix_and_suffix('&B_STEP=', '&B_LEVEL', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId, B_STEP)
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 3:
                var['uploader'].append(tdText)
            elif tdIdx == 4:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
            elif tdIdx == 5:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        '20' + tdText
                    )
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    span_l = extract_children_tag(soup, 'span', {'class' : 'span_l'}, childIsMultiple)
    for span in span_l:
        spanText = extract_text(span)
        if '작성자' in spanText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(span)
                )
            )
            break
    content = extract_children_tag(soup, 'dl', {'class' : 'content'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(content))
    var['postImageUrl'] = search_img_list_in_contents(content, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(result)
    return result


