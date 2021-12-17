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
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                onclick = extract_attrs(aTag, 'onclick')
                nttId, bbsId = parse_onclick(onclick)
                var['postUrl'].append(
                    var['postUrlFrame'].format(bbsId, nttId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        tdText[:-1]
                    )
                )
            elif tdIdx == 5 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList, var['channelCode'])
    # print(result)
    return result

def parse_onclick(text):
    data = re.findall("'(.+?)'", text)
    nttId, bbsId = data[0], data[1]
    return nttId, bbsId

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    table_info = extract_children_tag(soup, 'div' , {'class' : 'table_info'}, childIsNotMultiple)
    var['contact'] = extract_contact_numbers_from_text(extract_text(table_info))
    desc = extract_children_tag(soup, 'div', {'class' : 'desc'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(desc))
    imgList = extract_children_tag(desc, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result