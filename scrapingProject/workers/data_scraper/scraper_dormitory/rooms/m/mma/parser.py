from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'text_center'}, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', {'class' : False}, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 0 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = extract_text_between_prefix_and_suffix('gsgeul_no=', '&pageIndex', href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
            elif tdIdx == 2 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        tdText
                    )
                )
            elif tdIdx == 3 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'postTitle', 'uploader'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    table = extract_children_tag(soup, 'table', {'class' : 'notice_view'}, childIsNotMultiple)
    thList = extract_children_tag(table, 'th', dummyAttrs, childIsMultiple)
    for th in thList:
        thText = extract_text(th)
        if '제목' in thText:
            var['postTitle'] = extract_text(find_next_tag(th))
        elif '작성자' in thText:
            thText = extract_text(find_next_tag(th))
            var['uploader'] = thText
            var['contact'] = extract_contact_numbers_from_text(thText)
        if var['postTitle'] and var['uploader']:
            break
        
    con_text = extract_children_tag(table, 'td', {'class' : 'con_text'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(con_text))
    imgList = extract_children_tag(con_text, 'img', {'src' : True}, childIsMultiple)
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
    return result


