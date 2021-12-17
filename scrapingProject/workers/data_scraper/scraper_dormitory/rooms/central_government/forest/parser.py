from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        uploader = ''
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 0 and '공지' in tdText:
                break
            if tdIdx == 1:
                strong = extract_children_tag(tr, 'strong', dummyAttrs, childIsNotMultiple)
                uploader += extract_text(strong)[1:-1] + ' - '
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = extract_text_between_prefix_and_suffix('nttId=', '&bbsId', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                ) 
                var['postTitle'].append(
                    extract_text(aTag)
                )
            elif tdIdx == 2:
                uploader += tdText
                var['uploader'].append(uploader)
            elif tdIdx == 3:
                textSplit = tdText.split(' ')
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(textSplit[0])
                )
                var['viewCount'].append(
                    extract_numbers_in_text(textSplit[1])
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result


def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'postTextType'],
        'multipleType' : ['postImageUrl', 'extraInfo']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    var['postTextType'] = 'both'
    spanList = extract_children_tag(soup, 'span', {'class' : 'info_tit'}, childIsMultiple)
    for span in spanList:
        spanText = extract_text(span)
        if '작성자' in spanText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(span)
                )
            )
    contents = extract_children_tag(soup, 'div', {'class' : 'b_content'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(contents))

    imgList = extract_children_tag(contents, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)

    dlList = extract_children_tag(soup, 'dl', dummyAttrs, childIsMultiple)
    extraInfo = {'infoTitle' : '행사 정보'}
    for dl in dlList:
        dlText = extract_text(dl)
        if '주소' in dlText or '위치' in dlText:
            extraInfoText = extract_text(find_next_tag(dl))
            if extraInfoText:
                lenExtraInfo = len(extraInfo)
                extraInfo.update({f'info_{lenExtraInfo}' : extraInfoText})
        if 'info_0' in extraInfo.keys():
            var['extraInfo'].append(extraInfo)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result