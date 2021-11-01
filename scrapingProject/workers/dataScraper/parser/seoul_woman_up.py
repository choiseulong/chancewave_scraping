
from ..parserTools.tools import *
from ..scraperTools.tools import *

isMultiple = True

def extract_post_list_from_response_text(text, dateRange, channelCode, postUrlFrame):
    keyList = ['postTitle', 'uploadedTime', 'uploader', 'viewCount', 'postUrl']
    postTitle = []
    uploadedTime = []
    uploader = []
    viewCount = []

    soup = convert_response_text_to_BeautifulSoup(text)
    postInfoList = search_tags_in_soup(soup, "tr")

    if postInfoList :
        postInfoList = [
            postInfo \
            for postInfo \
            in postInfoList \
            if check_children_tags_existence_in_parents_tags(postInfo, 'th', {"scope" : "col"}) == 'not exists'
        ]
    tdIdxInfo = {1:"postTitle", 2:"uploader", 3:"uploadedTime", 5:"viewCount"}
    for postInfo in postInfoList:
        tdList = extract_children_tags_from_parents_tags(postInfo, 'td', isMultiple)
        for idx, td in enumerate(tdList):
            if idx == 0 and '공지' in td.text:
                break
            if idx in tdIdxInfo.keys():
                locals()[tdIdxInfo[idx]].append(clean_text(td.text))

    uploadedTimeCheckList = [
        True if check_date_range_availability(dateRange, dateString) == 'vaild' else False \
        for dateString \
        in uploadedTime
    ]
    postUrl = [
        postUrlFrame.format(extract_post_number_from_bs4_tag(tag))
        for tag in postInfoList[5:]
    ]
    uploadedTime = [
        convert_datetime_string_to_isoformat_datetime(dateString) \
        for dateString \
        in uploadedTime
    ]
    validPostCount = uploadedTimeCheckList.count(True)
    local_var = locals()
    valueList = [
        [i for idx, i in enumerate(local_var[key]) if uploadedTimeCheckList[idx]] \
        for key \
        in keyList
    ]
    for i in [len(valueList) for valueList in valueList]:
        if i != validPostCount:
            raise Exception(f"maybe channel {channelCode}, data parsing error")
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result


def extract_post_contents_from_response_text(text, channelMainUrl):
    keyList = ['postText', 'postImageUrl']
    postText = ''
    postImageUrl = []

    soup = convert_response_text_to_BeautifulSoup(text)
    div_viewContent = search_tags_in_soup(soup, 'div', {"class":"view_content"})
    if div_viewContent:
        div_viewContent = div_viewContent[0]
    postText = clean_text(div_viewContent.text)
    isFugure = check_children_tags_existence_in_parents_tags(div_viewContent, 'figure', {'class':'image'})
    if isFugure == 'exists':
        figure_image = extract_children_tags_from_parents_tags(div_viewContent, 'figure', isMultiple, {'class':'image'})
        figure_alt_text = ''
        for figure in figure_image:
            img_images = extract_children_tags_from_parents_tags(figure, 'img', isMultiple)
            for img in img_images:
                if img.has_attr('src'):
                    figure_src = img['src']
                    postImageUrl.append(channelMainUrl+figure_src) 
                    if img.has_attr('alt') and not postText.strip():
                        figure_alt = img['alt']
                        figure_alt_text += figure_alt
        postText = clean_text(figure_alt_text)
        
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    print(postImageUrl)
    return result


def extract_post_number_from_bs4_tag(tag):
    num = extract_values_list_in_both_sides_bracket_text(
        extract_attrs_from_tags(tag, "a", "onclick")
    )
    return num

def extract_values_list_in_both_sides_bracket_text(text):
    startIdx = text.find('(')
    endIdx = text.rfind(')')
    text = text[startIdx+1 : endIdx]
    valueList = [i.replace("'", "") for i in text.split(',')]
    return valueList[0]