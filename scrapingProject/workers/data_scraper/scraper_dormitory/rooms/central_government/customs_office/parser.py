from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['contentsReqParams', 'postTitle', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        subject = extract_children_tag(tr, 'td', {'data-table' : 'subject'}, childIsNotMultiple)
        var['postTitle'].append(
            extract_text(subject)
        )
        dataId = extract_attrs(
            extract_children_tag(subject, 'a'),
            'data-id'
        )
        var['contentsReqParams'].append(
            {
                "bbsId" : 1341,
                "nttSn" : dataId
            }
        )
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'date'})
                )
            )
        )
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'number'}, childIsNotMultiple)
                )
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'data-table' : 'write'}, childIsNotMultiple)
            )
        )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contetns = extract_children_tag(soup, 'td', {'class' : 'conts'}, childIsNotMultiple)
    postText = extract_text(contetns)
    if postText:
        var['contact'] = extract_contact_numbers_from_text(postText)
        var['postText'] = clean_text(postText)
    imgList = extract_children_tag(contetns, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList :
            src = extract_attrs(img, 'src')
            if 'http' not in src:
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result