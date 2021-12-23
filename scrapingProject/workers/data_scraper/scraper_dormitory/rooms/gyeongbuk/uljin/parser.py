from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    bbs_list = extract_children_tag(soup, 'ul', {'class' : 'bbs_list'}, childIsNotMultiple)
    liList = extract_children_tag(bbs_list, 'li', dummyAttrs, childIsMultiple)
    for li in liList :
        aTag = extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple)
        href = extract_attrs(aTag, 'href')
        var['postUrl'].append(
            var['channelMainUrl'] + href
        )
        infoText = extract_text_from_single_tag(li, 'em', dummyAttrs)
        infoList = infoText.split('|')
        uploader = ''
        for infoIdx, info in enumerate(infoList):
            if infoIdx == 0 :
                uploader += info.split(' : ')[1] + ' '
            elif infoIdx == 1 :
                uploader += info
            elif infoIdx == 2:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        info.split(' : ')[1]
                    )
                )
            elif infoIdx == 3 :
                var['viewCount'].append(
                    extract_numbers_in_text(info)
                )
        var['uploader'].append(uploader)

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'contact', 'postTitle'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbdoy = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    thList = extract_children_tag(tbdoy, 'th', dummyAttrs, childIsMultiple)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_text(find_next_tag(th))
        elif '제목' in thText:
            var['postTitle'] = extract_text(find_next_tag(th))
    cont = extract_children_tag(soup, 'td', {'class' : 'bbs_content'}, childIsNotMultiple)
    var['postText'] = extract_text(cont)
    var['postImageUrl'] = search_img_list_in_contents(cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result


