from ..parserTools.newtools import *

attrsIsEmpty = {}
tagIsUnique = True
childIsMultiple = True

def postListParsingProcess(**params):
    var = reflect_params(locals(), params)
    targetKeyInfo = {
        'listType' : ['postSubject', 'postTitle', 'uploader', 'postDataParams'],
        'strType' : ['_csrf']
    }
    var = reflect_key(var, targetKeyInfo)
    soup = change_to_soup(
        var['response'].text
    )
    post_list_box = extract_tag(soup, "div", {"class" : "result-list-box"}, tagIsUnique)
    post_list = extract_children_tag(post_list_box, "li", attrsIsEmpty, childIsMultiple)
    for post in post_list:
        var['postDataParams'].append(
            extract_attrs(
                extract_children_tag(post, "input", {"class" : "checkbox"}),
                "value"
            ) 
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
    var['_csrf'] = extract_text(
        extract_tag(soup, "meta", {"name" : "_csrf"}, tagIsUnique)
    )
    varList = [var[key] for key in targetKeyInfo['listType']]
    varList.append(var['_csrf'])
    result = merge_var_to_dict(targetKeyInfo['listType'], varList)
    return result
    