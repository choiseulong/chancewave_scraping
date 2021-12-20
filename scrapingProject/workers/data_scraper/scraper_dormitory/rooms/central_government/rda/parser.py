from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', {'class' : False}, childIsMultiple)
    for tr in trList :
        title = extract_children_tag(tr, 'a', {'title' : True}, childIsNotMultiple)
        var['postTitle'].append(extract_text(title))
        var['postUrl'].append(
            var['postUrlFrame'].format(extract_text_between_prefix_and_suffix(
                    'dataNo=', '&mode',
                    extract_attrs(
                        title,
                        'href'
                    )
                )
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'class' : 'board_tb_part'}, childIsNotMultiple)
            )
        )
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'board_tb_date'}, childIsNotMultiple)
                )
            )
        )
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'board_tb_hit'}, childIsNotMultiple)
                )
            )
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
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    thList = extract_children_tag(tbody, 'th', dummyAttrs, childIsMultiple)
    for th in thList:
        thText = extract_text(th)
        if '전화번호' in thText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(
                    find_next_tag(th)
                )
            )
            break
    
    contents = extract_children_tag(tbody, 'td', {'class' : 'con'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(contents))
    imgList = extract_children_tag(contents, 'img', {'src' : True}, childIsMultiple)
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = var['channelMainUrl'] + src
            var['postImageUrl'].append(src)

    valueList = [var[key] for key in keyList] 
    result = convert_merged_list_to_dict(keyList, valueList)
    
    # print(result)
    return result