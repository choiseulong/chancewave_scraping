from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

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
            if '공지' in tdText:
                if var['pageCount'] == 1 :
                    pass
                else :
                    break

            if tdIdx == 1 : 
                var['postTitle'].append(tdText)
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                var['postUrl'].append(
                    var['postUrlFrame'] + href
                )
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
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
    cont = extract_children_tag(soup, 'td', {'class' : 'cont'}, childIsNotMultiple)
    postText = extract_text(cont)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    var['postImageUrl'] = search_img_list_in_contents(cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


