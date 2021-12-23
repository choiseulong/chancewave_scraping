from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        uploader = ''
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            # if '공지' in tdText and tdIdx == 0:
            #     if var['pageCount'] == 1 :
            #         pass
            #     else :
            #         continue
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                # print(href)
                var['postUrl'].append(
                    var['channelMainUrl'] + href
                )
            elif tdIdx in [2] :
                uploader += tdText + ' '
            elif tdIdx == 4:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
        var['uploader'].append(uploader)
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'contact', 'postTitle', 'uploadedTime'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    news_tit = extract_children_tag(soup, 'div', {'class' : 'news_tit'}, childIsNotMultiple)
    var['postTitle'] = extract_text(
        extract_children_tag(news_tit, 'h3', dummyAttrs, childIsNotMultiple)
    )
    dtList = extract_children_tag(news_tit, 'dt', dummyAttrs, childIsMultiple)
    for dt in dtList:
        dtText = extract_text(dt)
        if '작성일' in dtText:
            var['uploadedTime'] = convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    find_next_tag(dt)
                )
            )
            break
    cont = extract_children_tag(soup, 'div', {'class' : 'board_cont'}, childIsNotMultiple)
    var['postText'] = extract_text(cont)
    var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
    var['postImageUrl'] = search_img_list_in_contents(cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(result)
    return result


