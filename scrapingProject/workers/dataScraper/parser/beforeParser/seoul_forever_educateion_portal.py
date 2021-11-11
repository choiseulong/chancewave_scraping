
from ..parserTools.tools import *
from ..scraperTools.tools import *

def extract_jsessionid_from_response_header(header):
    cookieBox = header['Set-Cookie']
    startIdx = cookieBox.find('JSESSIONID=')
    endIdx = cookieBox.find(';Path')
    JSESSIONID = cookieBox[startIdx+len('JSESSIONID=') : endIdx]
    return JSESSIONID

def extract_post_list_from_response_text(text, dateRange, channelCode):
    keyList = ['postTitle', 'contentsReqParams', 'uploadedTime', 'viewCount']
    local_var = locals()
    for key in keyList:
        local_var[key] = []
    soup = convert_response_text_to_BeautifulSoup(text)
    tr_items = search_tags_in_soup(soup, 'tr', {"onmouseover" : "className='odd_over'"})
    for tr in tr_items:
        local_var['postTitle'].append(
            clean_text(tr.find('td', attrs={'class' : ['ta_title']}).text)
        )
        local_var['contentsReqParams'].append(
            convert_bs4_tag_to_actual_post_body(tr)
        )
        local_var['uploadedTime'].append(
            tr.find('td', attrs={'class' : ['ta_date']}).text.replace('등록일 :', '').strip()
        )
        local_var['viewCount'].append(
            int(tr.find('td', attrs={'class' : ['ta_viewcnt']}).text.replace('조회수 :', '').strip())
        )
    uploadedTime = [
        convert_datetime_string_to_isoformat_datetime(date) if check_date_range_availability(dateRange, date) == 'vaild' \
        else False
        for date \
        in local_var['uploadedTime'] 
    ]
    valueList = [
        [i for idx, i in enumerate(local_var[key]) if uploadedTime[idx]] \
        for key \
        in keyList
    ]
    result = convert_same_length_merged_list_to_dict(keyList, valueList)
    return result


def get_contents_req_body(num, file_use):
    data = {
        "boarditem_no" : num,
        "board_no" : 14,
        "attach_file_use_yn" : file_use
    }
    return data

def convert_bs4_tag_to_actual_post_body(tag):
    boarditem_no, attach_file_use_yn = convert_contentsUrlParms_to_POST_data(
    extract_values_list_in_both_sides_bracket_text(
        extract_attrs_from_tags(tag, "a", "onclick")
        )
    )
    data = get_contents_req_body(boarditem_no, attach_file_use_yn)
    return data

def extract_values_list_in_both_sides_bracket_text(text):
    startIdx = text.find('(')
    endIdx = text.rfind(')')
    text = text[startIdx+1 : endIdx]
    valueList = [i.replace("'", "") for i in text.split(',')]
    return valueList

def convert_contentsUrlParms_to_POST_data(params):
    boarditem_no = params[0]
    attach_file_use_yn = params[1]
    return boarditem_no, attach_file_use_yn

def extract_post_contents_from_response_text(text):
    keyList = ['postText', 'postImageUrl']
    postText = ''
    postImageUrl = []

    soup = convert_response_text_to_BeautifulSoup(text)
    td_boarditem_content = search_tags_in_soup(soup, 'td', {"id" : "td_boarditem_content"})[0]
    postText = clean_text(td_boarditem_content.text)
    img_content = td_boarditem_content.findAll('img')
    if img_content:
        for img in img_content:
            if img.has_attr('src'):
                postImageUrl.append(img['src'])
    local_var = locals()
    valueList = [local_var[key] for key in keyList]
    result = convert_merged_list_to_dict(keyList, valueList)
    return result

    

    
    
    
    