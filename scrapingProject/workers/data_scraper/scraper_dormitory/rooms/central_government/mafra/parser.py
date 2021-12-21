from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        aTag = extract_children_tag(tr, 'a', dummyAttrs, childIsNotMultiple)
        href = extract_attrs(aTag, 'href')
        var['postUrl'].append(
            var['channelMainUrl'] + href
        )
        var['postTitle'].append(extract_text(aTag))
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'dd', {'class' : 'date'}, childIsNotMultiple)
                )
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'dd', {'class' : 'name'}, childIsNotMultiple)
            )
        )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result


def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'viewCount'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    view = extract_children_tag(soup, 'div', {'class': 'view'}, childIsNotMultiple)
    var['viewCount'] = extract_numbers_in_text(
        extract_text(
            extract_children_tag(view, 'dd', {'class' : 'hit'}, childIsNotMultiple)
        )
    )
    view_contents = extract_children_tag(view, 'div', {'class': 'view_contents'}, childIsNotMultiple)
    postText = extract_text(view_contents)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    var['postImageUrl'] = search_img_list_in_contents(view_contents, var['channelMainUrl'])
    valueList = [var[key] for key in keyList] 
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result