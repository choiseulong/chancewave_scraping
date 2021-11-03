from bs4 import BeautifulSoup as bs
from jsonpath_ng import parse as jsonpath_parse
from datetime import datetime
import xmltodict
import re

def convert_response_text_to_soup(data):
    return bs(data, 'html.parser')

def extract_tag_list_from_soup(soup, tag, attrs={}):
    return soup.findAll(tag, attrs)

def extract_text_from_tag(tag, isMultiple=False):
    return [_.text for _ in tag] if isMultiple else tag.text

def extract_content_from_tag(tag, isMultiple=False):
    return [_.content for _ in tag] if isMultiple else tag.content

def extract_attrs_from_tag(tag, attrsName, isMultiple=False):
    return [_[attrsName] for _ in tag] if isMultiple else tag[attrsName]

def extract_children_tag_text_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs={}, isMultiple=False):
    return [extract_text_from_tag(kid) for kid in parentsTag.findAll(childrenTag, attrs=childrenTagAttrs)] \
        if isMultiple \
        else extract_text_from_tag(parentsTag.find(childrenTag, attrs=childrenTagAttrs))

def extract_children_tag_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs={}, isMultiple=True):
    return parentsTag.findAll(childrenTag, attrs=childrenTagAttrs) \
        if isMultiple \
        else parentsTag.find(childrenTag, attrs=childrenTagAttrs)

def check_children_tag_existence_in_parents_tag(parentsTag, childrenTag, childrenTagAttrs={}):
    return 'exists' if parentsTag.find(childrenTag, attrs=childrenTagAttrs) \
        else 'not exists' 

def divide_individual_value_based_on_key(keyList, valueList):
    return [
        {
            key:valueList[keyIdx][dataIdx] \
            for keyIdx, key \
            in enumerate(keyList)
        } \
        for dataIdx \
        in range(len(valueList[0]))
    ]

def split_value_list_based_on_key(keyList, valueList):
    return {
        {key : valueList[keyIdx]} \
        for keyIdx, key \
        in enumerate(keyList)
    }

def convert_datetime_string_to_isoformat_datetime(datetimeString):
    specialWord = re.sub(r'[^.|-|:]', '', datetimeString)
    specialWordCount = {word:specialWord.count(word) for word in specialWord}
    timeFormat = ['%Y{}%m{}%d ', '%H{}%M{}%S ']
    strptimeFormat = ''
    for idx, key in enumerate(specialWordCount):
        strptimeFormat += timeFormat[idx].format(key, key)
    try :
        time = datetime.strptime(datetimeString, strptimeFormat.strip()).isoformat()
    except ValueError:
        strptimeFormat = strptimeFormat.replace(strptimeFormat[1], strptimeFormat[1].lower())
        time = datetime.strptime(datetimeString, strptimeFormat.strip()).isoformat()
    return time

def convert_datetime_to_isoformat(date):
    return date.isoformat()

def extract_numbers_in_text(text):
    return re.sub('[^0-9]', '', text)

def extract_korean_in_text(text):
    return ' '.join(re.compile('[가-힣]+').findall(text))

def erase_html_tags(text):
    return re.sub('(<([^>]+)>)', '', text)

def extract_groupCode(text):
    return '_'.join(text.split('_')[:-1])

def convert_multiple_empty_erea_to_one_erea(text):
    return re.sub('\s+', ' ', text).strip()

def clean_text(text):
    eraseSpace = ['\r', '&lsquo;', '&rsquo;']
    leaveSpace = ['\xa0', '\n', '\t', '&nbsp;']
    for _ in eraseSpace:
        text = text.replace(_, '')
    for _ in leaveSpace:
        text = text.replace(_, ' ')
    text = convert_multiple_empty_erea_to_one_erea(text)
    return text

def convert_response_content_to_dict(content):
    return xmltodict.parse(content)

def search_value_in_json_data_using_path(jsonData, path, number_of_data='multiple', reverse = False):
    tartget_data = jsonpath_parse(path).find(jsonData)
    result = []
    if tartget_data and number_of_data == 'solo':
        result = tartget_data[0].value
        if reverse :
            result = tartget_data[-1].value
    elif tartget_data and number_of_data == 'multiple':
        result = [ _.value for _ in tartget_data]
    return result



