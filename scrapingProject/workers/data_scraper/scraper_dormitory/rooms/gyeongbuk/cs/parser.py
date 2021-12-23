from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader', 'postThumbnail']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    liList = extract_children_tag(soup, 'li', {'class' : 'li1'}, childIsMultiple)
    for li in liList:
        aTag = extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple)
        href = extract_attrs(aTag, 'href')
        var['postUrl'].append(
            var['postUrlFrame'] + href
        )
        spanF1 = extract_children_tag(li, 'span', {'class' : 'f1'}, childIsNotMultiple)
        if spanF1:
            img = extract_children_tag(spanF1, 'img', dummyAttrs, childIsNotMultiple)
            src = extract_attrs(img, 'src')
            var['postThumbnail'].append(
                var['channelMainUrl'] + src
            )
        else :
            var['postThumbnail'].append(
                None
            )
        var['postTitle'].append(
            extract_text(
                extract_children_tag(li, 'strong', {"class" : "t1"}, childIsNotMultiple)
            )
        )
        wrap1t3 = extract_children_tag(li, 'i', {'class':'wrap1t3'}, childIsNotMultiple)
        spanList = extract_children_tag(wrap1t3, 'span', dummyAttrs, childIsMultiple)
        for spanIdx, span in enumerate(spanList):
            spanText = extract_text(span)
            if spanIdx == 0:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(spanText)
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
    var['postText'] = clean_text(extract_text(substance))
    var['contact'] = extract_contact_numbers_from_text(extract_text(substance))
    var['postImageUrl'] = search_img_list_in_contents(substance, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(result)
    return result
