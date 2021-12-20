from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                onclick = extract_attrs(aTag, 'onclick')
                postId = extract_text_between_prefix_and_suffix("('", "')", onclick)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(tdText)
            elif tdIdx == 2 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 3 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def parse_href(text):
    return text[text.find('&seq=') + len('&seq='):]

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'uploader', 'startDate', 'endDate'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    bv_category = extract_children_tag(soup, 'div', {'class' : 'bv_category'}, childIsNotMultiple)
    spanList = extract_children_tag(bv_category, 'span', dummyAttrs, childIsMultiple)
    uploader=''
    uploaderCount = 0 
    for spanIdx, span in enumerate(spanList):
        spanText = extract_text(span)
        nextSpanText =  extract_text(spanList[spanIdx+1])
        if '담당자' in spanText or '담당부서' in spanText : 
            uploader += nextSpanText + ' '
            uploaderCount += 1
        elif '전화번호' in spanText:
            var['contact'] = extract_contact_numbers_from_text(nextSpanText)
        elif '기간' in spanText:
            date = [i.strip() for i in nextSpanText.split('~') if i]
            if len(date) == 2 :
                date = [convert_datetime_string_to_isoformat_datetime(d) for d in date]
                var['startDate']= date[0]
                var['endDate'] = date[1]
            elif len(date) == 1 :
                var['startDate']= convert_datetime_string_to_isoformat_datetime(date[0])
            break
        if uploaderCount == 2:
            var['uploader'] = uploader     
    bv_content = extract_children_tag(soup, 'div', {'class' : 'bv_content'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(bv_content))
    imgList = extract_children_tag(bv_content, 'img', {'src' : True}, childIsMultiple)
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
