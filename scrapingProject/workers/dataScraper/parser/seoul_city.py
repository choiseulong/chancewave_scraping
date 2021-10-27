from ..parserTools.tools import *
from ..scraperTools.tools import *

parsingTypeContents = 'contents' 
parsingTypeText = 'text' 
parsingTypeNone = None
isMultiple = True

def extract_post_list_from_response_text(text, dateRange, channelCode):
    keyList = ["contentsUrl", "uploadedTime", "postSubject"]

    soup = convert_response_text_to_BeautifulSoup(text)
    postListInfo = search_tags_in_soup(soup, "div", {"class" : "item"})
    contentsUrl = extract_attrs_from_tags(postListInfo, "a", "href", isMultiple)
    uploadedTime = [
        convert_datetime_string_to_isoformat_datetime(dateString[:19]) \
        for dateString \
        in search_tags_in_soup(soup, "em", {"class" : "date"}, parsingTypeContents) \
        if check_date_range_availability(dateRange, dateString[:19]) == 'vaild'
    ]
    # uploadedTime = [
    #     convert_datetime_to_isoformat(date) \
    #     for date \
    #     in uploadedTime \
    #     if check_date_range_availability(dateRange, date) == 'vaild'
    # ]
    validPostCount = len(uploadedTime)
    if not validPostCount :
        return 

    print(f'\n {channelCode}, vaildPostCount : {validPostCount} \n 마지막 포스트 업로드 일자 : {uploadedTime[-1]}')
    postSubject = extract_text_from_tags(postListInfo, "i", isMultiple)
    if postSubject :
        postSubject = [extract_korean_in_text(subject) for subject in postSubject]

    local_var = locals()
    valueList = [local_var[key][:validPostCount] for key in keyList]

    for i in [len(valueList) for valueList in valueList]:
        if i != validPostCount:
            raise Exception("maybe channel a[0,1,2], data parsing error")
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result
 
def extract_post_contents_from_response_text(text, url):
    soup = convert_response_text_to_BeautifulSoup(text)
    keyList = ['postText', 'contact', 'uploader', 'postImageUrl', 'postTitle']

    view_top = search_tags_in_soup(soup, "div", {"id" : "view_top"}, parsingTypeNone)
    postTitle = extract_text_from_tags(view_top, 'h3', isMultiple)
    if postTitle:
        postTitle = postTitle[0]

    postText = search_tags_in_soup(soup, "div", {"id" : "post_content"}, parsingTypeText)
    if postText:
        postText = clean_text(' '.join(postText))
    postContent = search_tags_in_soup(soup, "div", {"id" : "post_content"}, parsingTypeNone)
    try :
        postImageUrl = extract_attrs_from_tags(postContent, 'img', 'src', isMultiple)
    except TypeError as e :
        postImageUrl = []
    contact = search_tags_in_soup(soup, "dl", {"class" : "top-row row2"}, parsingTypeText)
    if contact :
        contact = clean_text(contact[0])
    uploader = search_tags_in_soup(soup, "dd", {"class" : "dept"}, parsingTypeText)
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
    




    