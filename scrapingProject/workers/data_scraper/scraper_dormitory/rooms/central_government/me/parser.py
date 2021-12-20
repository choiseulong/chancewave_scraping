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
        uploader = ''
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = extract_text_between_prefix_and_suffix('boardId=', '&boardMasterId', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx in [2, 3]  :
                uploader += tdText + ' '
            elif tdIdx == 4:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 5 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
        var['uploader'].append(uploader)
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def parse_href(text):
    return text[text.find('&seq=') + len('&seq='):]

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    view_con = extract_children_tag(soup, 'div', {'class' : 'view_con'}, childIsNotMultiple)
    postText = extract_text(view_con)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    imgList = extract_children_tag(view_con, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
 
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(result)
    return result
