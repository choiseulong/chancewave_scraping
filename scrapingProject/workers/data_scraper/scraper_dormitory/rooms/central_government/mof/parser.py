from typing_extensions import Literal
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

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
            if '공지' in tdText :
                if var['pageCount'] == 1 :
                    pass
                else :
                    continue

            if tdIdx == 1 : 
                var['postTitle'].append(tdText)
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = extract_text_between_prefix_and_suffix('articleKey=', '&boardKey', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
            elif tdIdx == 2 :
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
                if tdText:
                    var['uploadedTime'].append(tdText)
                else :
                    var['uploadedTime'].append(None)
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
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'view'}, childIsNotMultiple)
    thList = extract_children_tag(tbody, 'th', dummyAttrs, childIsMultiple)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_text(find_next_tag(th))
            break
    boardCont = extract_children_tag(soup, 'div', {'class' : 'boardCont'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(boardCont))
    imgList = extract_children_tag(boardCont, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
 
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result
