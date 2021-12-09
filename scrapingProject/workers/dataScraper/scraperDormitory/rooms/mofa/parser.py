from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'viewCount', 'uploader', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                var['postUrl'].append(
                    var['postUrlFrame'].format(
                        extract_text_between_prefix_and_suffix('seq=', '&amp', extract_attrs(aTag, 'href'))
                    ) 
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
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
    contentsBox = extract_children_tag(soup, 'td', {'class' : 'detail_body'}, childIsNotMultiple)
    imgList = extract_children_tag(contentsBox, 'img', {'src' : True}, childIsMultiple)
    for img in imgList :
        src = extract_attrs(img, 'src')
        if 'http' not in src:
            src = var['channelMainUrl'] + src
        var['postImageUrl'].append(src)
    postText = extract_text(contentsBox)
    var['postText'] = clean_text(postText)
    var['contact'] = extract_contact_numbers_from_text(postText)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result