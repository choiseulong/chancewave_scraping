from ..parserTools.newtools import *
import json

attrsIsEmpty = {}
tagIsUnique = True
childIsMultiple = True

def postListParsingProcess(**params):
    var = reflect_params(locals(), params)
    targetKeyInfo = {
        'listType' : ['postSubject', 'postTitle', 'uploader', 'contentsReqParams'],
        'strType' : ['Cookie','_csrf']
    }
    var, _ = reflect_key(var, targetKeyInfo)
    soup = change_to_soup(
        var['response'].text
    )
    post_list_box = extract_children_tag(soup, "div", {"class" : "result-list-box"}, tagIsUnique)
    post_list = extract_children_tag(post_list_box, "li", attrsIsEmpty, childIsMultiple)
    
    var['_csrf'] = extract_attrs(
        extract_children_tag(soup, "meta", {"name" : "_csrf"}, tagIsUnique),
        "content"
    )
    for post in post_list:
        var['contentsReqParams'].append(
            {
                "_csrf" : var['_csrf'],
                "bizId" : extract_attrs(
                    extract_children_tag(post, "input", {"name" : "cmprCheckbox"}),
                    "value"
                )
            }
        ) 
        var['postTitle'].append(
            extract_text(
                extract_children_tag(post, "a"),
            )
        )
        var['postSubject'].append(
            extract_text(
                extract_children_tag(post, "span", {"class" : "srh-cate-data"}),
            ) 
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(post, "div", {"class" : "badge"})
            )
        )
    valueList = [var[key] for key in targetKeyInfo['listType']]
    result = merge_var_to_dict(targetKeyInfo['listType'], valueList)
    var['Cookie'] = var['response'].cookies.get_dict()['YOUTHCENTERSESSIONID']
    result.append({'Cookie' : 'YOUTHCENTERSESSIONID=' + var['Cookie']})
    return result

def postContentParsingProcess(**params):
    var = reflect_params(locals(), params)
    targetKeyInfo = {
        'listType' : ['extraInfo'],
        'strType' : ['postTextType']
    }
    var, keyList = reflect_key(var, targetKeyInfo)
    soup = change_to_soup(
        var['response'].text
    )
    infoTitle = [
        extract_text(h5) \
        for h5 \
        in extract_children_tag(soup, 'h5', {"class" : "view_tit"}, childIsMultiple)
    ]
    infoTable = [table for table in extract_children_tag(soup, 'div', {"class" : "table_wrap"}, childIsMultiple)]
    for tableIdx, table in enumerate(infoTable) :
        var['extraInfo'].append({'infoTitle' : infoTitle[tableIdx]}) 
        contentsTitle = [
            extract_text(_) \
            for _ \
            in extract_children_tag(table, 'div', {"class" : "list_tit"}, childIsMultiple)
        ]
        contents = [
            extract_text(_) \
            for _ \
            in extract_children_tag(table, 'div', {"class" : "list_cont"}, childIsMultiple)
        ]
        for title, cont in zip(contentsTitle, contents):
            infoNum = len(var['extraInfo'][tableIdx])
            var['extraInfo'][tableIdx].update({f'info_{infoNum}' : [title, cont]})
    var['postTextType'] = 'onlyExtraInfo'
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
        