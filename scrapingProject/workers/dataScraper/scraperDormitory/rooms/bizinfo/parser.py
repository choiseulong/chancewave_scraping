from workers.dataScraper.scraperDormitory.parserTools.tools import *

childIsNotMultiple = False
childIsMultiple = True
dummpyAttrs = {}

def postListParsingProcess(**params):
    targetKeyInfo = {
        'listType' : ['postUrl', 'postTitle', 'startDate', 'endDate', 'uploader', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummpyAttrs, childIsNotMultiple)
    contents_tr = extract_children_tag(tbody, 'tr', dummpyAttrs, childIsMultiple)
    for tr in contents_tr :
        anchor = extract_children_tag(tr, 'a', dummpyAttrs, childIsNotMultiple)
        var['postUrl'].append(
            var['postUrlFrame'].format(
                    extract_params(
                       extract_attrs(anchor, 'onclick')
                )
            )
        )
        var['postTitle'].append(
            extract_text(anchor)
        )
        contents_td = extract_children_tag(tr, 'td', dummpyAttrs, childIsMultiple)
        for idx, td in enumerate(contents_td):
            td_text = extract_text(td)
            if idx == 2:
                if '~' in td_text:
                    date = td_text.split(' ~ ')
                    date = [convert_datetime_string_to_isoformat_datetime(date[0]), convert_datetime_string_to_isoformat_datetime(date[1])]
                else :
                    date = [td_text, td_text]
                var['startDate'].append(
                    date[0]
                )
                var['endDate'].append(
                    date[1]
                )
            elif idx == 3:
                var['uploader'].append(td_text)
            elif idx == 4:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(td_text)
                )
            elif idx == 5:
                var['viewCount'].append(extract_numbers_in_text((td_text)))

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def extract_params(text):
    prefix = "('"
    suffix = "')"
    return text[text.find(prefix)+len(prefix):text.find(suffix)]

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'strType' : ['postSubject', 'postTextType'],
        'listType' : ['extraInfo']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    var['postTextType'] = 'onlyExtraInfo'
    tbody_list = extract_children_tag(soup, 'tbody', dummpyAttrs, childIsMultiple)
    tr = extract_children_tag(tbody_list[0], 'tr', dummpyAttrs, childIsNotMultiple) 
    td_list = extract_children_tag(tr, 'td', dummpyAttrs, childIsMultiple) 
    var['postSubject'] = extract_text(td_list[0])

    boardBusiness = extract_children_tag(soup, 'div', {"class" : "boardBusiness"}, childIsNotMultiple)
    h4_contName = extract_children_tag(boardBusiness, 'h4', {"class" : True}, childIsMultiple)
    extraDict = {"infoTitle" : "지원사업 상세"}

    for h4 in h4_contName:
        h4_text = extract_text(h4)
        next_tag = find_next_tag(h4)
        next_tag_class_attrs = extract_attrs(next_tag, 'class')[0]
        if next_tag_class_attrs == "contBox":
            next_tag_text = clean_text(extract_text(next_tag))
            extraInfoLength = len(extraDict)
            extraDict.update({f'info_{extraInfoLength}' : [h4_text, next_tag_text]})
    
    var['extraInfo'].append(extraDict)
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result



    