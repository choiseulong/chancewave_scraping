from bs4 import BeautifulSoup
from datetime import datetime
import re

def convert_response_text_to_BeautifulSoup(responseText):
    soup = BeautifulSoup(responseText, 'html.parser')
    return soup

def search_tags_in_soup(soup, tags, attrs={}, parsingType=''):
    if parsingType == 'contents':
        if not attrs :
            result = [i.contents[0] for i in soup.findAll(tags)]
        else:
            result = [i.contents[0] for i in soup.findAll(tags, attrs=attrs)]
    elif parsingType == 'text':
        if not attrs :
            result = [i.text for i in soup.findAll(tags)]
        else:
            result = [i.text for i in soup.findAll(tags, attrs=attrs)]
    else :
        if not attrs:
            result = soup.findAll(tags)
        else:
            result = soup.findAll(tags, attrs=attrs)
    return result

def extract_attrs_from_tags(items, tags, attrs, isMultiple = False):
    if isMultiple :
        result = [item.find(tags)[attrs] for item in items]
    else :
        result = items.find(tags)[attrs]
    return result 

def extract_contetns_from_tags(items, tags, isMultiple = False):
    if isMultiple :
        result = [i.find(tags).contents for i in items]
    else :
        result = items.find(tags).contents
    return result 

def extract_children_tags_from_parents_tags(parentsTags, childrenTags, isMultiple = False, attrs={}):
    if isMultiple :
        if attrs: 
            result = parentsTags.findAll(childrenTags, attrs=attrs)
        else :
            result = parentsTags.findAll(childrenTags)

    else :
        if attrs: 
            result = parentsTags.find(childrenTags, attrs=attrs)
        else:
            result = parentsTags.find(childrenTags)
    return result 


def extract_text_from_tags(items, tags, isMultiple=False):
    if isMultiple:
        result = [item.find(tags).text for item in items]
    else:
        result = items.find(tags).text
    return result

def check_children_tags_existence_in_parents_tags(parents_tags, children_tags, attrs={}):
    if attrs :
        if parents_tags.find(children_tags, attrs = attrs):
            return 'exists'
        else :
            return 'not exists'
    if parents_tags.find(children_tags):
        return 'exists'
    else :
        return 'not exists'


def convert_same_length_merged_list_to_dict(keyList, valueList):
    result = []
    for idx in range(len(valueList[0])):
        frame = {
            key: valueList[key_idx][idx] for key_idx, key in enumerate(keyList)
        }
        result.append(frame)
    return result

def convert_merged_list_to_dict(keyList, valueList):
    result = {}
    for idx, key in enumerate(keyList):
        result.update({key : valueList[idx]})
    return result

def convert_datetime_string_to_isoformat_datetime(datetimeString):
    if datetimeString.count('-') == 2 and datetimeString.count(':') == 2:
        time = datetime.strptime(datetimeString, "%Y-%m-%d %H:%M:%S").isoformat()
    elif datetimeString.count('-') == 2 and datetimeString.count(':') != 2:
        try :
            time = datetime.strptime(datetimeString, "%Y-%m-%d").isoformat()
        except ValueError :
            time = datetime.strptime(datetimeString, "%y-%m-%d").isoformat()
    elif datetimeString.count('.') == 2 and datetimeString.count(':') != 2:
        try :
            time = datetime.strptime(datetimeString, "%Y.%m.%d").isoformat()
        except ValueError :
            time = datetime.strptime(datetimeString, "%y.%m.%d").isoformat()
    return time

def convert_datetime_to_isoformat(postDate):
    if isinstance(postDate, datetime):
        return postDate.isoformat()
    else :
        raise Exception('convert_datetime_to_isoformat, postDate 타입 에러')

def extract_numbers_in_text(text):
    return re.sub('[^0-9]', '', text)

def extract_korean_in_text(text):
    return ' '.join(re.compile('[가-힣]+').findall(text))

def erase_html_tags(text):
    return re.sub('(<([^>]+)>)', '', text)

def extract_groupCode(text):
    return '_'.join(text.split('_')[:-1])

def clean_text(text):
    text = text.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ').replace('\r', '')
    text = convert_multiple_empty_erea_to_one_erea(text)
    return text

def convert_multiple_empty_erea_to_one_erea(text):
    return re.sub('\s+', ' ', text).strip()



  
