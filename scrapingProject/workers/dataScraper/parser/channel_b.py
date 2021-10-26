from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 

def b0_extract_post_list_from_response_text(text, dateRange):
    parsingType = '' 
    isMultiple = True
    keyList = ["contentsUrlParms", "uploadTime", "postSubject"]

    soup = convert_response_text_to_BeautifulSoup(text)
    postListInfo = search_tags_in_soup(soup, "tr", {}, parsingType)
    if postListInfo:
        postListInfo = postListInfo[1:]
    
    postSubject = ['공지' if len(data.attrs) else data.find('p').text for data in postListInfo]
    uploadTime = [
        convert_datetime_string_to_actual_datetime(
            tr.findAll('td')[-1].text.replace('.', '-')
        )
        for tr \
        in postListInfo
    ]
    uploadTime = [
        convert_datetime_to_isoformat(date) \
        for date \
        in uploadTime \
        if check_date_range_availability(dateRange, date) == 'vaild'
    ]
    contentsUrlParms = [data.find('a').attrs['onclick'] for data in postListInfo]
    contentsUrlParms = [
        extract_values_list_in_both_sides_bracket(data)
        for data in contentsUrlParms
    ]
    '''
        params 
        [
            ['13860', 'Y'],
            ...
            ['13841', 'Y']
        ]
    '''
    validPostCount = len(uploadTime)
    if validPostCount == 0 :
        return [] 
        
    local_var = locals()
    valueList = [local_var[key][:validPostCount] for key in keyList]
    for i in [len(valueList) for valueList in valueList]:
        if i != validPostCount:
            raise Exception("maybe channel b[0], data parsing error")
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result



def extract_values_list_in_both_sides_bracket(text):
    startIdx = text.find('(')
    endIdx = text.rfind(')')
    text = text[startIdx+1 : endIdx]
    valueList = [i.replace("'", "") for i in text.split(',')]
    return valueList


    

# tr 태그 가져오고
# 첫 번째는 제외하고 
# 두 번째 태그 컨텐츠부터 사용하고
# class 가 notice인 경우 공지 subject
# td 컨탠츠가 4개가 있음.
# 첫번째는 문서번호로 미사용
# 두 번째는 문서 주제
# 세번째는 제목 및 링크인데 
# 네 번째는 일자


# 상세 페이지는
# 제목 href속에있는 것들을 사용해서 요청
# body
# bbscttSn=13859&fileyn=N

# heaader
# Content-Type: application/x-www-form-urlencoded
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36
