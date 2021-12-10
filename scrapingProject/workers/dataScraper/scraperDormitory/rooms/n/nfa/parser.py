from workers.dataScraper.scraperDormitory.parserTools.tools import *

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
            if tdIdx == 0 and '공지' in tdText:
                break
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

def parse_onclick(text):
    return re.findall("'(.+?)'", text)[0]

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
    imgList = extract_children_tag(board_content, 'img', {'src' : True}, childIsMultiple)
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