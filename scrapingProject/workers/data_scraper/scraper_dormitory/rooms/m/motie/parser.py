from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postSubject', 'postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1 :
                var['postSubject'].append(tdText)
            elif tdIdx == 2 :
                var['postTitle'].append(tdText)
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = extract_text_between_prefix_and_suffix('bbs_seq_n=', '&bbs_cd_n', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
            elif tdIdx == 3:
                var['uploader'].append(tdText)
            elif tdIdx == 4:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 5:
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
    thList = extract_children_tag(soup, 'th', {'scope' : 'row'}, childIsMultiple)
    for th in thList :
        thText = extract_text(th)
        if '연락처' in thText:
            var['contact'] = extract_text(find_next_tag(th))
        elif '내용' in thText:
            nextTag = find_next_tag(th)
            var['postText'] = clean_text(extract_text(nextTag))
            imgList = extract_children_tag(nextTag, 'img', {'src' : True}, childIsMultiple)
            if imgList:
                for img in imgList:
                    src = extract_attrs(img, 'src')
                    if 'base64' in src :
                        var['postImageUrl'].append(src)
                        continue
                    if 'http' not in src :
                        src = var['channelMainUrl'] + src
                        var['postImageUrl'].append(src)
                        continue

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result