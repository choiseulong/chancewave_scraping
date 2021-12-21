from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'uploadedTime', 'postUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contetnsBox = extract_children_tag(soup, 'div', {'class' : 'board-list-wrap'}, childIsNotMultiple)
    innerDiv = extract_children_tag(contetnsBox, 'div', {'class' : 'inner'}, childIsMultiple)
    for div in innerDiv :
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(div, 'div', {'class' : 'info'}, childIsNotMultiple)
                )
            )
        )
        subject = extract_children_tag(div, 'div', {'class' : 'subject'}, childIsNotMultiple)
        var['postTitle'].append(
            extract_text(
                subject
            )
        )
        href = extract_attrs(
            extract_children_tag(subject, 'a', dummyAttrs, childIsNotMultiple),
            'href'
        )
        if 'http' not in href:
            href = var['channelMainUrl'] + href
        var['postUrl'].append(href)
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(div, 'div', {'class' : 'day'}, childIsNotMultiple)
                )
            )
        )


    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parse_href(text):
    prefix = "('"
    suffix = "')"
    result = text[text.find(prefix) + len(prefix) : text.find(suffix)]
    return result

    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText'],
        'multipleType' : ['postImageUrl', 'contact']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    contents = extract_children_tag(soup, 'td', {'class' : 'bbs_content'}, childIsNotMultiple)
    postText = extract_text(contents)
    if postText:
        var['postText'] = clean_text(postText)
        var['contact'] = extract_contact_numbers_from_text(postText)
    var['postImageUrl'] = search_img_list_in_contents(contents, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
