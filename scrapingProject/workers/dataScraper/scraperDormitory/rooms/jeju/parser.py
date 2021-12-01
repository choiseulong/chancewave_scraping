from workers.dataScraper.scraperDormitory.parserTools.tools import *

dummpyAttrs = {}
childIsNotMultiple = False
childIsMultiple = True

def postListParsingProcess(**params):
    targetKeyInfo = {
        'listType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummpyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', {"class" : True}, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummpyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            if tdIdx == 1 :
                var['postTitle'].append(extract_text(td))
                var['postUrl'].append(
                    var['channelMainUrl'] + \
                        extract_attrs(
                            extract_children_tag(td, 'a', dummpyAttrs, childIsNotMultiple),
                            'href'
                        )
                )
            elif tdIdx == 3:
                var['uploader'].append(
                    clean_text(extract_text(td))
                )
            elif tdIdx == 4: 
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(extract_text(td))
                )
            elif tdIdx == 5: 
                var['viewCount'].append(
                    extract_numbers_in_text(extract_text(td))
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'strType' : ['postText', 'contact'],
        'listType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    article = extract_children_tag(soup, 'td', {"class" : "article-contents"}, childIsNotMultiple)
    imgList = extract_children_tag(article, 'img', dummpyAttrs, childIsMultiple)
    if imgList:
        for img in imgList:
            var['postImageUrl'].append(
                extract_attrs(
                    img, 'src'
                )
            )
    var['postText'] = clean_text(
        extract_text(article)
    )
    thList = extract_children_tag(soup, 'th', dummpyAttrs, childIsMultiple)
    for th in thList :
        if extract_text(th) == '연락처':
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(th)
                )
            )
            if len(var['contact']) == 1 :
                var['contact'] = var['contact'][0]
            break
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result