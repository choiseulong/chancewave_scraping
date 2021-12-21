from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs ,childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            # if tdIdx == 0 and '공지' in tdText:
            #     break
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                postId = extract_text_between_prefix_and_suffix("cntId=", "&amp", extract_attrs(aTag, 'href'))
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 2:
                var['uploader'].append(tdText)
            elif tdIdx == 3:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 4:
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
    board_content = extract_children_tag(soup, 'div', {'class' : 'board_content'}, childIsNotMultiple)
    postText = extract_text(board_content)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    var['postImageUrl'] = search_img_list_in_contents(board_content, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result