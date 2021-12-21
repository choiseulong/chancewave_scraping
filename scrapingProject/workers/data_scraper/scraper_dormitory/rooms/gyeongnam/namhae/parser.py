from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    liList = extract_children_tag(soup, 'li', {'class' :'li1'}, childIsMultiple)
    for li in liList:
        aTag = extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple)
        href = extract_attrs(aTag, 'href')
        postId = extract_text_between_prefix_and_suffix('&idx=', '&pageCd', href)
        var['postUrl'].append(
            var['postUrlFrame'].format(postId)
        )
        strong = extract_children_tag(li, 'strong', {'class' :'t1'}, childIsNotMultiple)
        var['postTitle'].append(
            extract_text(strong)
        )
        t3wrap = extract_children_tag(li, 'i', {'class' : 't3wrap'}, childIsNotMultiple)
        spanList = extract_children_tag(t3wrap, 'span', dummyAttrs, childIsMultiple)
        for spanIdx, span in enumerate(spanList):
            spanText = extract_text(span)
            if spanIdx == 0 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        spanText
                    )
                )
            elif spanIdx == 1 :
                var['uploader'].append(spanText)
            elif spanIdx == 2 :
                var['viewCount'].append(
                    extract_numbers_in_text(spanText)
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
    substance = extract_children_tag(soup, 'div', {'class' : 'substance'}, childIsNotMultiple)
    postText = extract_text(substance)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    var['postImageUrl'] = search_img_list_in_contents(substance, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


