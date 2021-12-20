from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount', 'uploader']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if '공지' in tdText:
                if var['pageCount'] == 1 :
                    pass
                else :
                    continue

            if tdIdx == 1 : 
                var['postTitle'].append(tdText)
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                postId = parse_href(href)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 4 :
                var['uploadedTime'].append(tdText)
            elif tdIdx == 5 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def parse_href(text):
    return text[text.find('&dataSid=') + len('&dataSid='):]




def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    titleField = extract_children_tag(soup, 'div', {'class' : 'titleField'}, childIsNotMultiple)
    strongList = extract_children_tag(titleField, 'strong', dummyAttrs, childIsMultiple)
    for strong in strongList:
        strongText = extract_text(strong)
        if '연락처' in strongText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(find_next_tag(strong))
            )
            break
    
    conText = extract_children_tag(soup, 'div', {'class' : 'conText'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(conText))
    imgList = extract_children_tag(conText, 'img', {'src' : True}, childIsMultiple)
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
