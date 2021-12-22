from typing_extensions import Literal
from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    dbody = extract_children_tag(soup, 'div', {'class' : 'dbody'}, childIsNotMultiple)
    ulList = extract_children_tag(dbody, 'ul', dummyAttrs, childIsMultiple)
    for ul in ulList:
        liList = extract_children_tag(ul, 'li', dummyAttrs, childIsMultiple)
        for liIdx, li in enumerate(liList):
            liText = extract_text(li)
            if '공지' in liText :
                if var['pageCount'] == 1 :
                    pass
                else :
                    break
            if liIdx == 1:
                aTag = extract_children_tag(li, 'a', dummyAttrs, childIsNotMultiple)
                onclick = extract_attrs(aTag, 'onclick')
                postId = extract_text_between_prefix_and_suffix("('", "')", onclick)
                var['postUrl'].append(
                    var['postUrlFrame'].format(postId)
                )
                var['postTitle'].append(liText)
            elif liIdx == 3 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(liText)
                )
            elif liIdx == 4 :
                var['viewCount'].append(
                    extract_numbers_in_text(liText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def parse_href(text):
    return text[text.find('&seq=') + len('&seq='):]

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'uploader'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    headInfo = extract_children_tag(soup, 'ul', {'class': ['head', 'info']}, childIsNotMultiple)
    spanList = extract_children_tag(headInfo, 'span', dummyAttrs, childIsMultiple)
    for span in spanList:
        spanText = extract_text(span)
        if '담당부서' in spanText:
            print(extract_text(find_next_tag(span)))
            var['uploader'] = extract_text(find_next_tag(span))
        elif '연락처' in spanText:
            var['contact'] = extract_contact_numbers_from_text(
                extract_text(find_next_tag(span))
            )

    tb_contents = extract_children_tag(soup, 'div', {'class' : 'tb_contents'}, childIsNotMultiple)
    var['postText'] = clean_text(extract_text(tb_contents))
    var['postImageUrl'] = search_img_list_in_contents(tb_contents, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    # print(result)
    return result
