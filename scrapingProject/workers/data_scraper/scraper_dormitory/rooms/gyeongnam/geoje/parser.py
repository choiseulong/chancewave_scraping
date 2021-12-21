from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1 : 
                var['postTitle'].append(tdText)
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                var['postUrl'].append(
                    var['channelMainUrl'] + href
                )
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 2 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 5 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
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
    info = extract_children_tag(soup, 'div', {'class' : 'info'}, childIsNotMultiple)
    strongList = extract_children_tag(info, 'strong', dummyAttrs, childIsMultiple)
    for strong in strongList:
        strongText = extract_text(strong)
        if '연락처' in strongText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_parent_tag(strong)
                )
            )
            break
    substan = extract_children_tag(soup, 'div', {'class' : 'substan'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(substan))
    var['postImageUrl'] = search_img_list_in_contents(substan, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


