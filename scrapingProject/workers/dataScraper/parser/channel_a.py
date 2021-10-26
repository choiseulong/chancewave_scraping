from ..parserTools.tools import *
from ..scraperTools.tools import *

def extract_post_list_from_response_text(text, dateRange):
    parsingType = 'contents' 
    isMultiple = True
    keyList = ["contentsUrl", "uploadTime", "postSubject", "postTitle"]

    soup = convert_response_text_to_BeautifulSoup(text)
    postListInfo = search_tags_in_soup(soup, "div", {"class" : "item"})
    contentsUrl = extract_attrs_from_tags(postListInfo, "a", "href", isMultiple)
    uploadTime = [
        convert_datetime_string_to_actual_datetime(dateString[:19]) \
        for dateString \
        in search_tags_in_soup(soup, "em", {"class" : "date"}, parsingType)
    ]
    uploadTime = [
        convert_datetime_to_isoformat(date) \
        for date \
        in uploadTime \
        if check_date_range_availability(dateRange, date) == 'vaild'
    ]
    validPostCount = len(uploadTime)
    postSubject = extract_text_from_tags(postListInfo, "i", isMultiple)
    if postSubject :
        postSubject = [extract_korean_in_text(subject) for subject in postSubject]
    postTitle = search_tags_in_soup(soup, "em", {"class" : "subject"}, parsingType)
    local_var = locals()
    valueList = [local_var[key][:validPostCount] for key in keyList]
    dataLength = len(postListInfo)

    for i in [len(valueList) for valueList in valueList]:
        if i != dataLength:
            raise Exception("Channel a0, data parsing error")
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result
 
def extract_post_contents_from_response_text(text):
    parsingType = 'text' 
    soup = convert_response_text_to_BeautifulSoup(text)
    keyList = ['postText', 'contact', 'uploader']
    postText = search_tags_in_soup(soup, "div", {"id" : "post_content"}, parsingType)
    if postText:
        postText = clean_text(' '.join(postText))
    contact = search_tags_in_soup(soup, "dl", {"class" : "top-row row2"}, parsingType)
    if contact :
        contact = clean_text(contact[0])
    uploader = search_tags_in_soup(soup, "dd", {"class" : "dept"}, parsingType)
    if uploader :
        uploader = ', '.join(uploader)
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

def search_total_post_count(result):
    postNumberIdx = result['postTitle'].find(']')
    postNumber = extract_numbers_in_text(result['postTitle'][:postNumberIdx])
    totalPageCount = divmod(int(postNumber), 10)[0] + 1
    return totalPageCount
    




    