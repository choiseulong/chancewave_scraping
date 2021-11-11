from ..parserTools.newtools import *
from ..scraperTools.tools import *

parsingTypeContents = 'contents' 
parsingTypeText = 'text' 
parsingTypeNone = None
parentsIsMultiple = True
parentsIsNotMultiple = False
childrenIsMultiple = True
childrenIsNotMultiple = False
dummyAttrs = {}

def extract_post_list_from_response_text(text, dateRange, channelCode):
    keyList = ["postUrl", "uploadedTime", "postSubject"]
    local_var= locals()
    for key in keyList:
        local_var[key] = [] 

    soup = convert_response_text_to_soup(text)
    parentsTagList = extract_tag_list_from_soup(soup, "div", {"class" : "item"})

    local_var["postUrl"] = extract_children_tag_attrs_from_parents_tag(parentsTagList, 'a', 'href', dummyAttrs, parentsIsMultiple)
    em_date = extract_tag_list_from_soup(soup, "em", {"class":"date"})
    local_var["uploadedTime"] = [
        convert_datetime_string_to_isoformat_datetime(extract_text_from_tag(em)[:19]) \
        if check_date_range_availability(dateRange, extract_text_from_tag(em)[:19]) == 'vaild' \
        else False
        for em \
        in em_date
    ]
    local_var["postSubject"] = [
        extract_korean_in_text(text) \
        for text \
        in extract_children_tag_text_from_parents_tag(parentsTagList, "i", dummyAttrs, parentsIsMultiple, childrenIsNotMultiple)
    ]
    valueList = [
        [i for idx, i in enumerate(local_var[key]) if local_var["uploadedTime"][idx]] \
        for key \
        in keyList
    ]
    result = divide_individual_value_based_on_key(keyList, valueList)
    return result
 
def extract_post_contents_from_response_text(text):
    keyList = ['postText', 'contact', 'uploader', 'postImageUrl', 'postTitle']

    soup = convert_response_text_to_BeautifulSoup(text)
    div_viewTop = extract_tag_list_from_soup(soup, "div", {"id" : "view_top"})
    postTitle = extract_children_tag_text_from_parents_tag(div_viewTop, 'h3', dummyAttrs, parentsIsMultiple)
    postTitle = postTitle[0] if postTitle else 'title error'
    div_postText = extract_tag_list_from_soup(soup, "div", {"id" : "post_content"})
    div_postText = div_postText[0] if div_postText else 'text error'
    postText = ' '.join([clean_text(text) for text in extract_children_tag_text_from_parents_tag(div_postText, 'p', {"class" : ['indent20', 'mt20']}, parentsIsNotMultiple, childrenIsMultiple)])
    if not postText :
        postText = ' '.join([clean_text(text) for text in extract_children_tag_text_from_parents_tag(div_postText, 'p', dummyAttrs, parentsIsNotMultiple, childrenIsMultiple)])
    print(postText)
    # postContent = search_tags_in_soup(soup, "div", {"id" : "post_content"}, parsingTypeNone)
    # try :
    #     postImageUrl = extract_children_tag_attrs_from_parents_tag(postContent, 'img', 'src', isMultiple)
    # except TypeError as e :
    #     postImageUrl = []

    # contact = search_tags_in_soup(soup, "dl", {"class" : "top-row row2"}, parsingTypeText)
    # if contact :
    #     contact = clean_text(contact[0])
    # uploader = search_tags_in_soup(soup, "dd", {"class" : "dept"}, parsingTypeText)
    # if uploader :
    #     uploader = ', '.join(uploader)
    # local_var = locals()
    # valueList = [local_var[key] for key in keyList]
    # result = convert_merged_list_to_dict(keyList, valueList)
    # return result

def search_total_post_count(result):
    postNumberIdx = result['postTitle'].find(']')
    postNumber = extract_numbers_in_text(result['postTitle'][:postNumberIdx])
    totalPageCount = divmod(int(postNumber), 10)[0] + 1
    return totalPageCount
    




    