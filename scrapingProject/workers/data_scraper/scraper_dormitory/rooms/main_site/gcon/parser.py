from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['isGoingOn', 'viewCount', 'uploadedTime', 'postTitle', 'postUrl', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    contentsList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)

    for contents in contentsList:
        ongoingCheck = extract_children_tag(contents, 'span', {"class": ['tag color01']}, childIsNotMultiple)
        if var['channelCode'] == 'gyeonggi_content_agency_0':
            if not ongoingCheck :
                var['isGoingOn'].append(False)
                # continue
            else :
                var['isGoingOn'].append(True)
        else :
            var['isGoingOn'].append(None)
        viewCount = extract_children_tag(contents, 'td', {"class": "hit"}, childIsNotMultiple)
        var['viewCount'].append(extract_numbers_in_text(extract_text(viewCount)))
        uploadedTime = extract_children_tag(contents, 'td', {"class": "date"}, childIsNotMultiple)
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(uploadedTime).strip()
            )
        )
        postTitle = extract_children_tag(contents, 'a', {"title": True}, childIsNotMultiple)
        var['postTitle'].append(
            extract_text(postTitle)
        )
        var['postUrl'].append(
            var['channelMainUrl'] + extract_attrs(postTitle, 'href')
        )
        uploader = extract_children_tag(contents, 'td', {"class": "name"}, childIsNotMultiple)
        var['uploader'].append(extract_text(uploader))
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['extraInfo'],
        'singleType' : ['postTextType', 'postThumbnail']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    var['postTextType'] = 'onlyExtraInfo'
    commBoxList = extract_children_tag(soup, 'div', {"class" : "commBox"}, childIsMultiple)
    extraDict = {'infoTitle' : '사업 상세'}
    for commBox in commBoxList:
        ul = extract_children_tag(commBox, 'ul', dummyAttrs, childIsNotMultiple)
        if type(ul) == type(None):
            continue
        sTlt = extract_children_tag(ul, 'div', {"class" : "sTlt"}, childIsNotMultiple)
        sTltText = extract_text(sTlt)
        sTltContentsText = extract_text(find_next_tag(sTlt))
        lenExtraDict = len(extraDict)
        extraDict.update({f'info_{lenExtraDict}' : [sTltText, sTltContentsText]})
    var['extraInfo'].append(extraDict)
    imgDiv = extract_children_tag(soup, 'div', {"class" : "img"}, childIsNotMultiple)
    if imgDiv:
        var['postThumbnail'] = var['channelMainUrl'] + extract_attrs(
            extract_children_tag(imgDiv, 'img', dummyAttrs, childIsNotMultiple),
            'src'
        )
    else :
        var['postThumbnail'] = None

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result


def postContentParsingProcess_other(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'linkedPostUrl'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    view_content = extract_children_tag(soup, 'div', {"class" : "view-content"}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(view_content))
    aTagList = extract_children_tag(view_content, 'a', {'target' : True}, childIsMultiple)
    if aTagList:
        for aTag in aTagList:
            print(aTag)
            href = extract_attrs(aTag, 'href')
            if href :
                var['linkedPostUrl'] += href
    imgList = extract_children_tag(view_content, 'img', dummyAttrs, childIsMultiple)
    if imgList:
        for img in imgList:
            var['postImageUrl'].append(var['channelMainUrl'] + extract_attrs(img, 'src')) 

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
