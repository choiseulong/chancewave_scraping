from workers.dataScraper.scraperTools.tools import *
from workers.dataScraper.parserTools.tools import * 


def extract_post_list_from_response_text(content, dateRange, channelCode):
    keyList = ['postTitle', 'postUrl', 'uploadedTime', "uploader", "postSubject", "postText", "contact"]
    local_var = locals()
    for key in keyList:
        local_var[key] = []

    dictData = convert_response_content_to_dict(content)
    items = dictData['rss']['channel']['item']
    linkInfo = {
        "title" : "postTitle", "link" : "postUrl", "pubDate":"uploadedTime", "dc:creator" : "uploader",
        "category" : "postSubject", "content:encoded" : "postText", "manager_name" : "contact", "manager_phone" : "contact"
    }
    for item in items:
        checkedValueList = []
        for itemKey in item:
            if itemKey in linkInfo.keys():
                try :
                    _ = checkedValueList.index(linkInfo[itemKey])
                    local_var[linkInfo[itemKey]][-1] += f' : {item[itemKey]}'
                except ValueError :
                    local_var[linkInfo[itemKey]].append(item[itemKey])
                    checkedValueList.append(linkInfo[itemKey])
    local_var['postText'] = [erase_html_tags(i) for i in local_var['postText']]
    uploadedTime = [
        date if check_date_range_availability(dateRange, date) == 'vaild' \
        else False \
        for date \
        in local_var['uploadedTime']
    ]
    local_var['postSubject'] = [
        '-'.join(data) \
        for data \
        in local_var['postSubject']
    ]
    valueList = [
        [i for idx, i in enumerate(local_var[key]) if uploadedTime[idx]] \
        for key \
        in keyList
    ]
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result

def extract_post_list_from_response_text_other(jsonData, dateRange, channelCode):
    pass