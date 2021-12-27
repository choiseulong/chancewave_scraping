# -*- coding: utf-8 -*-
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl']
    }
    var, soup, keyList, fullText = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    if not trList :
        return
    for tr in trList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if '공지' in tdText and tdIdx == 0:
                if var['pageCount'] == 1 :
                    pass
                else :
                    continue
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'data-action')
                postId = extract_text_between_prefix_and_suffix('bIdx=', '&ptIdx', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'viewCount', 'uploadedTime', 'uploader', 'postTitle'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    view_info = extract_children_tag(soup, 'div', {'class' : 'view_info'}, childIsNotMultiple)
    liList = extract_children_tag(view_info, 'li', dummyAttrs, childIsMultiple)
    uploader = ''
    for li in liList:
        liText = extract_text(li)
        liTextSplited = liText.split(':')[1].strip()
        print(liText)
        if '연락처' in liText:
            var['contact'] = liTextSplited
        elif '작성자' in liText or '담당자' in liText:
            uploader += liTextSplited + ' '
        elif '등록일' in liText:
            var['uploadedTime']=(
                convert_datetime_string_to_isoformat_datetime(liTextSplited)
            )
        elif '조회' in liText:
            var['viewCount']=(
                extract_numbers_in_text(liText)
            )
    var['uploader'] = uploader
    bod_view = extract_children_tag(soup, 'div', {'class' : 'bod_view'}, childIsNotMultiple)
    var['postTitle'] = extract_text(extract_children_tag(bod_view, 'h4', dummyAttrs, childIsNotMultiple))
    view_cont = extract_children_tag(bod_view, 'div', {'class' : 'view_cont'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(view_cont))
    var['postImageUrl'] = search_img_list_in_contents(view_cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


