from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'postTitle', 'uploadedTime', 'viewCount']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    print
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList:
        viewBox = extract_children_tag(tr, 'div', {'class' : 'viewbox'}, childIsNotMultiple)
        var['postTitle'].append(extract_text(viewBox))
        params = parse_onclick_params(
            extract_attrs(
                extract_children_tag(viewBox, 'a', dummyAttrs, childIsNotMultiple),
                'onclick'
            )
        )
        var['postUrl'].append(
            var['postUrlFrame'].format(params)
        )
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            if tdIdx == 4 :
                var['uploadedTime'].append(
                    convert_datetime_string_to_isoformat_datetime(
                        tdText.strip()
                    )
                )
            elif tdIdx == 5 :
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def parse_onclick_params(text):
    return re.findall("'(.+?)'", text)[0]


def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['contact', 'postText', 'uploader'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    table = extract_children_tag(soup, 'table', {'class' : 'board_view'}, childIsNotMultiple)
    title_sp = extract_children_tag(table, 'div', {'class' : 'title_sp'}, childIsNotMultiple)
    spanList = extract_children_tag(title_sp, 'span', dummyAttrs, childIsMultiple)
    for span in spanList:
        spanText = extract_text(span)
        if '작성자' in spanText or '담당부서' in spanText:
            spanText = spanText.split(': ')[1]
            var['uploader'] += spanText + ' '
        elif '전화번호' in spanText:
            var['contact'] = extract_contact_numbers_from_text(spanText)
    pList = extract_children_tag(table, 'p', dummyAttrs, childIsMultiple)
    for p in pList:
        pText = extract_text(p)
        if pText:
            var['postText'] += pText + ' '


    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result