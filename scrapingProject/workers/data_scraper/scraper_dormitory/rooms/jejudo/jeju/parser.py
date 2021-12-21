from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

# jeju_1 ~ jeju_5
def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', {"class" : True}, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            if tdIdx == 1 :
                var['postTitle'].append(extract_text(td))
                var['postUrl'].append(
                    var['channelMainUrl'] + \
                        extract_attrs(
                            extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple),
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
        'singleType' : ['postText', 'contact'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    article = extract_children_tag(soup, 'td', {"class" : "article-contents"}, childIsNotMultiple)
    var['postImageUrl'] = search_img_list_in_contents(article, var['channelMainUrl'])
    var['postText'] = clean_text(
        extract_text(article)
    )
    thList = extract_children_tag(soup, 'th', dummyAttrs, childIsMultiple)
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

# jeju_6
def postListParsingProcess_other(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
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

def postContentParsingProcess_other(**params):
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
    var['postImageUrl'] = search_img_list_in_contents(viewContent, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def parse_href(text):
    prefix = 'ice_id='
    suffix = '¤'
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result