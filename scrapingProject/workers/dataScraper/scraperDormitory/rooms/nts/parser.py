from workers.dataScraper.scraperDormitory.parserTools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['contentsReqParams', 'postTitle', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        bbs_tit = extract_children_tag(tr, 'td', {'class' : 'bbs_tit'}, childIsNotMultiple)
        atag = extract_children_tag(bbs_tit, 'a', {'class' : 'nttInfoBtn'}, childIsNotMultiple)
        href = extract_numbers_in_text(
            extract_attrs(
                atag, 
                'href'
            )
        )
        data = {
            "bbsId" : 1011,
            "nttSn" : href
        }
        var['postTitle'].append(
            extract_text(atag).replace('N', '')
        )
        var['contentsReqParams'].append(data)
        
        var['uploadedTime'].append(
            convert_datetime_string_to_isoformat_datetime(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'date'}, childIsNotMultiple)
                )[:-1]
            )
        )
        var['viewCount'].append(
            extract_numbers_in_text(
                extract_text(
                    extract_children_tag(tr, 'td', {'data-table' : 'number'}, childIsMultiple)[-1]
                )
            )
        )
        
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    print(result)
    # return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
