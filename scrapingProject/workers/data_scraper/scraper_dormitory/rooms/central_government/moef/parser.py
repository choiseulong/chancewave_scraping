from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
import re

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contentsBox = extract_children_tag(soup, 'ul', {'class' : 'boardType3'})
    liList = extract_children_tag(contentsBox, 'li', dummyAttrs, childIsMultiple)
    for li in liList:
        var['postTitle'].append(
            extract_text(extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple))
        )
        aTag = extract_children_tag(li, 'a')
        if not aTag:
            print(li)
        MOSF, MOSFBBS = parse_href(
            extract_attrs(
                aTag,
                'href'
            )
        )
        var['postUrl'].append(
            var['postUrlFrame'].format(MOSFBBS, MOSF)
        )
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(li, 'span', {'class' : 'date'})
                )[:-1]
            )
        )
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parse_href(text):
    data = re.findall("'(.+?)'", text)
    MOSF, MOSFBBS = data[0], data[1]
    return MOSF, MOSFBBS
    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['viewCount', 'uploader', 'contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    container = extract_children_tag(soup, 'div', {'class' : 'subContainer'}, childIsNotMultiple)
    var['viewCount'] = extract_numbers_in_text(
        extract_text(
            extract_children_tag(container, 'span', {'class' : 'view'}, childIsNotMultiple)
        )
    )
    departInfo = extract_children_tag(container, 'ul', {'class' : 'departInfo'}, childIsNotMultiple)
    departLi = extract_children_tag(departInfo, 'li', dummyAttrs, childIsMultiple)
    for liIdx, li in enumerate(departLi):
        liText = extract_text(li)
        if liIdx in [1, 3]:
            var['contact'] += liText + ' '
        elif liIdx in [0, 2] :
            var['uploader'] += liText + ' '
    
    editorCont = extract_children_tag(container, 'div', {'class' : 'editorCont'}, childIsNotMultiple)
    var['postText'] = extract_text(editorCont)
    var['postImageUrl'] = search_img_list_in_contents(editorCont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
