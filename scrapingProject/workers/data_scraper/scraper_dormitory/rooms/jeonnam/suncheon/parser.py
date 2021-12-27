from workers.data_scraper.scraper_dormitory.parser_tools.tools import *
from datetime import datetime
from pytz import timezone

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['postUrl', 'uploadedTime', 'viewCount', 'uploader', 'postTitle']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    tbody = extract_children_tag(soup, 'tbody', dummyAttrs, childIsNotMultiple)
    trList = extract_children_tag(tbody, 'tr', dummyAttrs, childIsMultiple)
    for tr in trList :
        tdList = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple)
        uploader = ''
        for tdIdx, td in enumerate(tdList):
            tdText = extract_text(td)
            # if '공지' in tdText and tdIdx == 0:
            #     if var['pageCount'] == 1 :
            #         pass
            #     else :
            #         continue
            if tdIdx == 1 :
                aTag = extract_children_tag(td, 'a', dummyAttrs, childIsNotMultiple)
                href = extract_attrs(aTag, 'href')
                var['postUrl'].append(
                    var['channelMainUrl'] + href
                )
                var['postTitle'].append(
                    tdText
                )
            elif tdIdx in [3] :
                uploader += tdText + ' '
            elif tdIdx == 5:
                var['viewCount'].append(
                    extract_numbers_in_text(tdText)
                )
            elif tdIdx == 4:
                if ':' in tdText: 
                    now = datetime.now(timezone('Asia/Seoul'))
                    tdText = now.isoformat()
                else :
                    tdText = convert_datetime_string_to_isoformat_datetime(tdText)
                var['uploadedTime'].append(tdText)
        var['uploader'].append(uploader)
    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    # print(result)
    return result

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['postText', 'contact'],
        'multipleType' : ['postImageUrl']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)

    cont = extract_children_tag(soup, 'div', {'class' : 'board_cont'}, childIsNotMultiple)
    var['postText'] = extract_text(cont)
    var['contact'] = extract_contact_numbers_from_text(extract_text(cont))
    var['postImageUrl'] = search_img_list_in_contents(cont, var['channelMainUrl'])
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(result)
    return result


