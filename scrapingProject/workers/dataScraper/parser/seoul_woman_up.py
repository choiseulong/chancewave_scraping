
from ..parserTools.newtools import *
from ..scraperTools.tools import *

dummpyAttrs = {}
isMultiple = True
isNotMultiple = False
ParentsIsMultiple = True
ParentsIsNotMultiple = False
childIsMultiple = True
childIsNotMultiple = False
childIsUnique = True

def postListParsingProcess(**params):
    local_var = change_params_to_local_var(locals(), params)
    # key 지역변수 선언
    keyList = ['postTitle', 'uploadedTime', 'uploader', 'viewCount', 'postUrl']
    local_var = add_empty_list(local_var, keyList)

    # post info idx
    tdIdxInfo = {1:"postTitle", 2:"uploader", 3:"uploadedTime", 5:"viewCount"}
    if 'seoul_woman_up_1' == local_var['channelCode'] :
        tdIdxInfo = {0:"uploader", 1:"postTitle", 2:"uploadedTime", 4:"viewCount"}

    # html parsing
    soup = change_to_soup(local_var['response'].text)

    # main post list tags
    postInfoList = extract_tag_list(soup, "tr")
    postInfoList = [
        postInfo \
        for postInfo \
        in postInfoList \
        if check_children_tag_existence(postInfo, 'th', {"scope" : "col"}) == 'not exists'
    ]
    if len(postInfoList) > 10 :
        postInfoList = postInfoList[5:]


    #post info parsing
    for postInfo in postInfoList:
        tdTags = extract_children_tag(postInfo, 'td', dummpyAttrs, childIsMultiple)
        for idx, td in enumerate(tdTags):
            if idx == 0 and '공지' in td.text:
                break
            if idx in tdIdxInfo.keys():
                locals()[tdIdxInfo[idx]].append(clean_text(td.text))
    local_var['uploadedTime'] = [
        convert_datetime_string_to_isoformat_datetime(dateString) \
            if check_date_range_availability(local_var['dateRange'], dateString) == 'vaild' \
            else False \
        for dateString \
        in local_var['uploadedTime']
    ]
    local_var['postUrl'] = [
        local_var['postUrlFrame'].format(extract_post_number_from_bs4_tag(tag))
        for tag in postInfoList
    ]
    valueList = [
        [
            value \
            for idx, value \
            in enumerate(local_var[key]) \
            if local_var['uploadedTime'][idx]
        ] \
        for key \
        in keyList
    ]
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result

def postContentParsingProcess(**params):
    local_var = change_params_to_local_var(locals(), params)
    keyList = ['postText', 'postImageUrl', 'contact']
    postImageUrl = []

    soup = change_to_soup(local_var['response'].text)

    div_viewContent = extract_tag_list(soup, 'div', {"class":"view_content"}, childIsUnique)
        
    postText = clean_text(
        extract_text(div_viewContent)
    )
    contact = ' & '.join(extract_contact_numbers_from_text(postText)) if extract_contact_numbers_from_text(postText) else ''
    if check_children_tag_existence(div_viewContent, 'figure', {'class':'image'}) == 'exists':
        figure_image = extract_children_tag(div_viewContent, 'figure', {'class':'image'}, childIsMultiple)
        for figure in figure_image:
            img_images = extract_children_tag(figure, 'img', dummpyAttrs, childIsMultiple)
            for img in img_images:
                if check_has_attrs_in_tag(img, 'src'):
                    postImageUrl.append(local_var['channelMainUrl'] + extract_attrs(img, 'src')) 
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def postContentParsingProcess_second(**params):
    local_var = change_params_to_local_var(locals(), params)
    keyList = ['postTitle', 'uploader', 'postSubject', 'extraInfoList', 'startDate2', 'endDate2', 'uploadTime']
    local_var = add_empty_list(local_var, keyList)

    idxInfo = {0:"postSubject", 1:"postSubject", 2:"extraInfoList", 3:"startDate2", 4:"endDate2", 5:"extraInfoList", 6:"extraInfoList"}

    soup = change_to_soup(local_var['response'].text)
    div_lisBox = extract_tag_list(soup, 'div', {'class' : 'lis_box'}, childIsUnique)
    div_items = extract_children_tag(div_lisBox, 'div', dummpyAttrs, childIsMultiple)
    for item in div_items:
        itemContents = extract_contents(item, isNotMultiple)
        for item_idx, item_contents in enumerate(itemContents):
            if item_idx == 1 :
                extraInfo = {}
                subject = []
                dt = extract_children_tag(item_contents, 'dt')
                difficulty = clean_text(
                    extract_text(
                        extract_children_tag(dt, 'b')
                    )
                )
                extraInfo.update({'infoTitle' : '교육 프로그램'})
                extraInfo.update({f'info_{len(extraInfo)}' : ['필요능력정도',difficulty]})
                dt_text = clean_text(
                    extract_text(dt)
                    .replace(difficulty, '')
                )
                local_var['postTitle'].append(dt_text)
                span_text = [
                    clean_text(extract_text(span)) \
                    for span \
                    in extract_children_tag(item_contents, 'span', dummpyAttrs, childIsMultiple)
                ]
                em_text = [
                    clean_text(extract_text(em)) \
                    for em \
                    in extract_children_tag(item_contents, 'em', dummpyAttrs, childIsMultiple)
                ]
                contentsCount = 0
                for i,j in zip(span_text, em_text):
                    if contentsCount in idxInfo.keys():
                        if idxInfo[contentsCount] == 'extraInfoList':
                            extraInfo.update({f'info_{len(extraInfo)}':[i,j]})
                        elif idxInfo[contentsCount] == 'postSubject':
                            subject.append(j)
                        else :
                            local_var[idxInfo[contentsCount]].append(j)
                    contentsCount += 1
                local_var['postSubject'].append('-'.join(subject))
                local_var['extraInfoList'].append(extraInfo)
            if item_idx == 3:
                local_var['uploader'].append(
                    clean_text(extract_text(item_contents)
                    )
                )
    local_var['uploadTime'] = [
        check_event_date_range_availability(startDate, endDate) \
            if check_event_date_range_availability(startDate, endDate) \
            else False \
        for startDate, endDate \
        in zip(local_var['startDate2'], local_var['endDate2']) \
    ]
    print(local_var['uploadTime'])
    local_var['uploadTime'] = [
        date if check_date_range_availability(local_var['dateRange'], date) == 'vaild' \
        else False \
        for date \
        in local_var['uploadTime']\
    ]
    valueList = [
        [i for idx, i in enumerate(local_var[key]) if local_var['uploadTime'][idx]] \
        for key \
        in keyList
    ]
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    print(result)
    return result

def check_event_date_range_availability(recruitDateRange, studyDateRange): 
    now = datetime.now(timezone('Asia/Seoul')).isoformat()
    recruitDateStart = convert_datetime_string_to_isoformat_datetime(
        recruitDateRange.split('~')[0].strip()
    )
    studyDateEnd = convert_datetime_string_to_isoformat_datetime(
        studyDateRange.split('~')[1].strip()
    )
    if recruitDateStart <= now <= studyDateEnd:
        return recruitDateStart
    elif now <  recruitDateStart:
        return now
    elif studyDateEnd < now :
        return 

def extract_post_number_from_bs4_tag(tag):
    aTag = extract_children_tag(tag, "a")
    num = extract_values_list_in_both_sides_bracket_text(
        extract_attrs(aTag, "onclick")
    )
    return num

def extract_values_list_in_both_sides_bracket_text(text):
    startIdx = text.find('(')
    endIdx = text.rfind(')')
    text = text[startIdx+1 : endIdx]
    valueList = [i.replace("'", "") for i in text.split(',')]
    return valueList[0]
