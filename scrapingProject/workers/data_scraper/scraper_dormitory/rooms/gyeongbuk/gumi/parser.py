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
        uploader = ''
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if '공지' in tdText:
                if var['pageCount'] == 1 :
                    pass
                else :
                    continue
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                onclick = extract_attrs(aTag, 'onclick')
                postId = parse_onclick(onclick, 4)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx in [3, 4]:
                uploader += tdText + ' '
            elif tdIdx == 6:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
            elif tdIdx == 5:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
        var['uploader'].append(uploader)
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
    view_info = extract_children_tag(soup, 'div', {'class' : 'view_info'}, childIsNotMultiple)
    liList = extract_children_tag(view_info, 'li', dummyAttrs, childIsMultiple)
    for li in liList:
        liText = extract_text(li)
        if '작성자' in liText:
            var['contact'] = extract_contact_numbers_from_text(liText)
            break
    view_cont = extract_children_tag(soup, 'div', {'class' : 'view_cont'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(view_cont))
    var['postImageUrl'] = search_img_list_in_contents(view_cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result

