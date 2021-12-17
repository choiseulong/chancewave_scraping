from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['viewCount', 'postTitle', 'uploader', 'postUrl', 'uploadedTime']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'text_center'}, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 1:
                href = extract_attrs(
                    extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple),
                    'href'
                )
                if 'html' not in href :
                    href = parse_href(href)
                    href = var['postUrlFrame'].format(href)
                var['postUrl'].append(href)
                var['postTitle'].append(tdText.replace('새글', ''))
            elif tdIdx == 3 :
                var['uploader'].append(tdText)
            elif tdIdx == 4:
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(tdText)
                )
            elif tdIdx == 5 :
                var['viewCount'].append(extract_numbers_in_text(tdText))

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parse_href(text):
    prefix = 'nttNo='
    suffix = '&searchCtgry'
    return text[text.find(prefix) + len(prefix) : text.find(suffix)]
    
def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', {'class' : 'p-table--th-left'}, childIsNotMultiple)
    thList = extract_children_tag(tbody, 'th', dummyAttrs, childIsMultiple)
    tdCount = 0
    for th in thList :
        tdText = extract_text(th)
        if tdText in ['부서', '연락처'] :
            nextTh = find_next_tag(th)
            nextThText = extract_text(nextTh)
            var['contact'] += nextThText + ' '
            tdCount += 1
        if tdCount == 2 :
            break
    content = extract_children_tag(tbody, 'td', {'class' : 'p-table__content'}, childIsNotMultiple)
    var['postText'] = extract_text(content)
    
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result
    