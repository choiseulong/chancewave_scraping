from workers.data_scraper.scraper_dormitory.parser_tools.tools import *

def postListParsingProcess(**params):
    targetKeyInfo = {
        'multipleType' : ['isGoingOn', 'postTitle', 'postUrl', 'postThumbnail', 'uploader', 'startDate', 'endDate', 'postSubject']
    }
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    dataList = extract_children_tag(soup, 'div', {"class" : "multi_cont"}, childIsNotMultiple) # tag
    competitionList = extract_children_tag(dataList, 'a', {"class" : "goCompetitionDetail"}, childIsMultiple) # list
    for data in competitionList :
        status = extract_text(extract_children_tag(data, 'span', {"class" : "flag_md"}))
        if status == '진행중': 
            var['isGoingOn'].append(True)
        else :
            var['isGoingOn'].append(False)

        var['postUrl'].append(
            var['channelMainUrl'] + \
            extract_attrs(
                data, 'href'
            )
        )
        var['postThumbnail'].append(
            var['channelMainUrl'] + \
            extract_attrs(
                extract_children_tag(data, 'img'),
                'src'
            )
        )
        var['postTitle'].append(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "tit"})
            )
        )
        var['uploader'].append(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "user"})
            )
        )
        var['postSubject'].append(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "type"})
            ) + ' & ' + \
            extract_text(
                extract_children_tag(data, 'span', {"class" : "flag_md"})
            )   
        )
        startDate, endDate = parsing_date(
            extract_text(
                extract_children_tag(data, 'p', {"class" : "date"})
            )
        )
        var['startDate'].append(
            convert_datetime_string_to_isoformat_datetime(startDate)
        )
        var['endDate'].append(
            convert_datetime_string_to_isoformat_datetime(endDate)
        )

    valueList = [var[key] for key in keyList]
    result = merge_var_to_dict(keyList, valueList)
    return result

def parsing_date(text): 
    result = [k.strip()[:-1] for k in text.split('~')]
    return result[0], result[1]

def postContentParsingProcess(**params):
    targetKeyInfo = {
        'singleType' : ['viewCount', 'linkedPostUrl', 'contact', 'postContentTarget', 'postText'],
        'multipleType' : ['postImageUrl']
    } 
    var, soup, keyList, _ = html_type_default_setting(params, targetKeyInfo)
    table = extract_children_tag(soup, 'tbody', dummyAttrs) # return default -> tag
    trList = extract_children_tag(table, 'tr', dummyAttrs, childIsMultiple) # list
    for tr in trList :
        th = extract_children_tag(tr, 'th', dummyAttrs, childIsMultiple) # list
        td = extract_children_tag(tr, 'td', dummyAttrs, childIsMultiple) # list
        th_text = extract_text(th, isMultiple)
        td_text = extract_text(td, isMultiple)

        info = {'조회수' : 'viewCount', '문의':'contact', '홈페이지':'linkedPostUrl', '응모대상' : 'postContentTarget'}
        for key in info :
            if key in th_text:
                th_idx = th_text.index(key)
                var[info[key]] = td_text[th_idx]

    detail_content = extract_children_tag(soup, 'div', {'class' : 'detail'}) # return default -> tag
    detail_img = extract_children_tag(detail_content, 'img', dummyAttrs, childIsMultiple)
    if detail_img :
        for img in detail_img :
            var['postImageUrl'].append(
                var['channelMainUrl'] + extract_attrs(img, 'src')
            )
    detail_text = extract_children_tag(detail_content, 'div', {"class" : "text"})
    var['postText'] = clean_text(
        extract_text(detail_text)
    )
    valueList = [var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result