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
                postId = extract_text_between_prefix_and_suffix('&parm_bod_uid=', '&srchEnable=', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 3:
                var['uploader'].append(tdText)
            elif tdIdx == 5:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
            elif tdIdx == 4:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
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
    view_body = extract_children_tag(soup, 'div', {'class' : 'view_body'}, childIsNotMultiple)
    postText = str(view_body)
    postText = extract_text_between_prefix_and_suffix("write('",  "');", postText)
    soup = change_to_soup(postText)
    if soup :
        postText = extract_text(soup)
        var['postText'] = clean_text(postText).replace('&#39;', "'")
        var['contact'] = extract_contact_numbers_from_text(postText)
        var['postImageUrl'] = search_img_list_in_contents(soup, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


