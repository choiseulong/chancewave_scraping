from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        Continue = False
        if imgList:
            imgList = extract_children_tag(tr, 'img', dummyAttrs, childIsMultiple)
            for img in imgList:
                alt = extract_attrs(img, 'alt')
                if alt == '공지':
                    Continue = True
                    break
        if Continue:
            continue
        var['postUrl'].append(
            var['postUrlFrame'].format(
                parse_href(
                    extract_attrs(
                        extract_children_tag(tr, 'a', dummyAttrs, childIsNotMultiple), 'href')
                )
            )
        )
        var['postTitle'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'class' : 'title'}, childIsNotMultiple)
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(tr, 'td', {'class' : 'writer'}, childIsNotMultiple)
            )
        )
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'date'}, childIsNotMultiple)
                )
            )
        )
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'class' : 'hits'}, childIsNotMultiple)
                )
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
    dtList = extract_children_tag(soup, 'dt', dummyAttrs, childIsMultiple)
    for dt in dtList :
        if extract_text(dt) == '연락처':
            print(extract_text(find_next_tag(dt)))
            var['contact'] = extract_text(find_next_tag(dt))
    
    viewContent = extract_children_tag(soup, 'div', {'class' : 'view-content'}, childIsNotMultiple)
    var['postText'] = extract_text(viewContent)
    imgList = extract_children_tag(viewContent, 'img', dummyAttrs, childIsMultiple)
    if imgList:
        var['postImageUrl'] = [var['channelMainUrl'] + extract_attrs(img, 'src') for img in imgList]

    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def parse_href(text):
    prefix = 'ice_id='
    suffix = '¤'
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result