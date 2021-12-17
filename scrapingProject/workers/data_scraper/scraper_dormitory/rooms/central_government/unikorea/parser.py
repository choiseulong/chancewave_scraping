from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'viewCount', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        title = extract_children_tag(tr, 'td', {'class' : 'title'}, childIsNotMultiple)
        var['postTitle'].append(extract_text(title))
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'created'}, childIsNotMultiple)
                )
            )
        )
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'hit'}, childIsNotMultiple)
                )
            )
        )
        postId = extract_text_between_prefix_and_suffix(
            'cntId=', 
            '&amp', 
            extract_attrs(
                extract_children_tag(title, 'a', dummyAttrs, childIsNotMultiple),
                'href'
            )
        )
        var['postUrl'].append(
            var['postUrlFrame'].format(postId)
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
    var['contact'] = extract_contact_numbers_from_text(postText)
    var['postText'] = clean_text(postText)
    imgList = extract_children_tag(board_content, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result