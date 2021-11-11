
from ..parserTools.tools import *
from ..scraperTools.tools import *

def extract_post_list_from_response_text(jsonData, dateRange, channelCode):
    keyList = ['postTitle', 'postUrl', 'uploader', 'contact', 'uploadedTime']
    local_var = locals()
    for key in keyList :
        local_var[key] = []    
    rawData = jsonData['result']
    infoLink = {
        "title" : "postTitle", 
        "link":"postUrl", 
        "dept":"uploader", 
        "phone":"contact", 
        "pubdate":"uploadedTime"
    }
    for data in rawData:
        for key in data:
            if key in infoLink.keys():
                local_var[infoLink[key]].append(data[key])
    uploadedTime = [
        date \
        for date \
        in local_var['uploadedTime'] \
        if check_date_range_availability(dateRange, date) == 'vaild'
    ]
    validPostCount = len(uploadedTime)
    valueList = [local_var[key][:validPostCount] for key in keyList]
    for i in [len(valueList) for valueList in valueList]:
        if i != validPostCount:
            raise Exception(f"channel {channelCode}, data parsing error")
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result

def extract_post_contents_from_response_text(text):
    keyList = ['postImgaeUrl', 'postText']
    postImgaeUrl = []
    postText = ''
    soup = convert_response_text_to_BeautifulSoup(text)
    post_content = search_tags_in_soup(soup, 'div', {'id' : 'post_content'})
    img_postContent = post_content[0].findAll('img')
    if img_postContent:
        for img in img_postContent:
            postImgaeUrl.append(img['src'])
    if post_content[0].text:
        postText += clean_text(post_content[0].text)
    
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result



            


   