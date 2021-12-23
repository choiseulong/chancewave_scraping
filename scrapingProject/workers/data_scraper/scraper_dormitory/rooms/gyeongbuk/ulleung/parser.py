from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        if len(tdList) < 4 :
            break 
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if not tdText and tdIdx == 0:
                break
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                var['postUrl'].append(
                    var['channelMainUrl'] + href
                )
            elif tdIdx in [2] :
                var['uploader'].append(tdText)
            elif tdIdx == 4:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
            elif tdIdx == 3:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'contact', 'postTitle'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    var['postTitle'] = extract_text_from_single_tag(soup, 'p', {'class' : 'view_tle'})
    cont = extract_children_tag(soup, 'div', {'class' : 'view_body'}, childIsNotMultiple)
    var['postText'] = extract_text(cont)
    var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
    var['postImageUrl'] = search_img_list_in_contents(cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


