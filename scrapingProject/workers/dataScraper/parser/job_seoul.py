from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 
from datetime import datetime
from pytz import timezone

parsingTypeNone = None
parsingTypeText = 'text' 
isMultiple = True

def extract_post_list_from_response_text(text, dateRange, channelCode = ''):
    keyList = ["contentsReqParams", "uploadedTime", "postSubject"]

    soup = convert_response_text_to_BeautifulSoup(text)
    postListInfo = search_tags_in_soup(soup, "tr", {}, parsingTypeNone)
    if postListInfo:
        postListInfo = postListInfo[1:]
    
    isExists = check_children_tags_existence_in_parents_tags(postListInfo[0], 'p')
    if isExists == 'exists':
        postSubject = ['공지' if len(data.attrs) else data.find('p').text for data in postListInfo]
    elif isExists == 'not exists':
        postSubject = [None for _ in range(len(postListInfo))]

    uploadedTime = [
        convert_datetime_string_to_isoformat_datetime(
            tr.findAll('td')[-1].text.replace('.', '-')
        )
        for tr \
        in postListInfo \
        if check_date_range_availability(dateRange, tr.findAll('td')[-1].text.replace('.', '-')) == 'vaild'
    ]
    contentsReqParams = [
        convert_bs4_tag_to_actual_post_body(data)
        for data in postListInfo
    ]
    validPostCount = len(uploadedTime)
    if validPostCount == 0 :
        return 
    print(f'\n {channelCode}, vaildPostCount : {validPostCount} \n 마지막 포스트 업로드 일자 : {uploadedTime[-1]}')
    result = collect_locals_data(locals(), keyList, validPostCount, channelCode)
    return result

def collect_locals_data(local_var, keyList, validPostCount, channelCode):
    valueList = [local_var[key][:validPostCount] for key in keyList]
    for i in [len(valueList) for valueList in valueList]:
        if i != validPostCount:
            raise Exception(f"channel {channelCode}, data parsing error")
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result

def convert_bs4_tag_to_actual_post_body(tag):
    body = convert_contentsUrlParms_to_POST_data(
        extract_values_list_in_both_sides_bracket_text(
            extract_attrs_from_tags(tag, "a", "onclick")
        )
    )
    return body

def extract_values_list_in_both_sides_bracket_text(text):
    startIdx = text.find('(')
    endIdx = text.rfind(')')
    text = text[startIdx+1 : endIdx]
    valueList = [i.replace("'", "") for i in text.split(',')]
    return valueList

def convert_contentsUrlParms_to_POST_data(params):
    data = {
        "bbscttSn" : params[0],
        "fileyn" : params[1]
    }
    return data

def extract_post_contents_from_response_text(text):
    keyList = ['postText', 'postTitle']
    soup = convert_response_text_to_BeautifulSoup(text)
    postTitle = search_tags_in_soup(soup, 'h1', {'class' : 'bbs_subject'}, parsingTypeText)[0]
    postText = search_tags_in_soup(soup, 'div', {'class' : 'article_detail'}, parsingTypeText)
    if postText:
        postText = clean_text(' '.join(postText))
    else :
        print(f'{postTitle}, postText not exists')
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result


def other_extract_post_list_from_response_text(text, dateRange, channelCode = ''):
    keyList = ['postUrl', 'postTitle', 'uploadedTime']
    soup = convert_response_text_to_BeautifulSoup(text)
    postListInfo = search_tags_in_soup(soup, "tr", {}, parsingTypeNone)
    postUrl = []
    postTitle = []
    uploadedTime = []

    if postListInfo:
        postListInfo = postListInfo[1:]
        for post in postListInfo:
            url = extract_attrs_from_tags(post, 'a', 'href')[1:]
            title = extract_text_from_tags(post, 'a').strip()
            tdData = extract_children_tags_from_parents_tags(post, 'td', isMultiple)
            recruitDateRange = tdData[2].text
            studyDateRange = tdData[3].text
            uploadTime = check_education_date_range_availability(recruitDateRange, studyDateRange)
            if uploadTime :
                postUrl.append(url)
                postTitle.append(title)
                uploadedTime.append(uploadTime)
    validPostCount = len(uploadedTime)
    if not validPostCount:
        return
    print(f'\n {channelCode}, vaildPostCount : {validPostCount} \n 마지막 포스트 업로드 일자 : {uploadedTime[-1]}')
    result = collect_locals_data(locals(), keyList, validPostCount, channelCode)
    result.append(search_jsessionid(soup))
    return result

def check_education_date_range_availability(recruitDateRange, studyDateRange): 
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

def search_jsessionid(soup):
    formTag = search_tags_in_soup(soup, 'form', {'name' : 'rEdcLst'}, parsingTypeNone)
    attrsAction = formTag[0]['action']
    startIndex = attrsAction.find('jsessionid=')
    endIndex = attrsAction.find('?method')
    jsessionid = attrsAction[startIndex+len('jsessionid='):endIndex]
    return jsessionid

def other_extract_post_contents_from_response_text(text):
    keyList = ['postText', 'extraInfoList', 'extraInfoList', 'postImageUrl'] 
    soup = convert_response_text_to_BeautifulSoup(text)
    trTags = search_tags_in_soup(soup, 'tr', {}, parsingTypeNone)
    infoTags = search_tags_in_soup(soup, 'h2', {"class" : "tit1"}, parsingTypeText)
    infoTable = search_tags_in_soup(soup, 'table', {"class" : "tb_bbs view"}, parsingTypeNone)
    extraInfoList = []
    postImageUrl = []
    postText = ''
    for title, table in zip(infoTags, infoTable):
        extraObj = {"infoTitle" : title}
        trTags = extract_children_tags_from_parents_tags(table, "tr", isMultiple)
        for tr in trTags:
            th = tr.find('th', attrs={'scope' : 'row'})
            if not th :
                continue
            else :
                thText = clean_text(th.text)
                trText = clean_text(tr.find('td').text)
                if thText and trText:
                    if thText == '교육내용':
                        if trText:
                            postText = trText
                        imageTag = tr.find('img')
                        if imageTag :
                            imageUrl = imageTag['src']
                            postImageUrl.append(imageUrl)
                    else :
                        extraObjKeysLength = len(list(extraObj.keys()))
                        extraObj.update({f'info_{extraObjKeysLength}' : (thText, trText)})
        extraInfoList.append(extraObj)
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result



    

