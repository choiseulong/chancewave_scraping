from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 

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
    # uploadedTime = [
    #     convert_datetime_to_isoformat(date) \
    #     for date \
    #     in uploadedTime \
    #     if check_date_range_availability(dateRange, date) == 'vaild'
    # ]
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
        print(postTitle)
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

    