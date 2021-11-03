from bs4 import BeautifulSoup as bs
from bs4 import Tag
from jsonpath_ng import parse as jsonpath_parse
from datetime import datetime
import xmltodict
import re

def convert_response_text_to_soup(data):
    return bs(data, 'html.parser')

def extract_tag_list_from_soup(soup, tag, attrs={}):
    return soup.findAll(tag, attrs=attrs)

def extract_text_from_tag(tag, isMultiple=False):
    return [_.text for _ in tag] if isMultiple else tag.text

def extract_content_from_tag(tag, isMultiple=False):
    return [_.content for _ in tag] if isMultiple else tag.content

def extract_attrs_from_tag(tag, attrsName, isMultiple=False):
    return [_[attrsName] for _ in tag] if isMultiple else tag[attrsName]

def extract_children_tag_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs={}, ParentsIsMultiple=False):
    return parentsTag.find_all(childrenTag, attrs=childrenTagAttrs) \
        if ParentsIsMultiple \
        else parentsTag.find(childrenTag, attrs=childrenTagAttrs)

def extract_children_tag_text_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs={}, ParentsIsMultiple=False, childIsMultiple=False):
    return [
                extract_text_from_tag(
                    extract_children_tag_from_parents_tag(parents, childrenTag, childIsMultiple),
                    childIsMultiple
                )
                for parents \
                in parentsTag
            ] \
            if ParentsIsMultiple \
            else [
                extract_text_from_tag(kids, childIsMultiple) \
                for kids \
                in extract_children_tag_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs, childIsMultiple)
            ] 

def extract_children_tag_content_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs={}, ParentsIsMultiple=False):
    return [extract_content_from_tag(kid) for kid in extract_children_tag_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs)] \
        if ParentsIsMultiple \
        else extract_content_from_tag(parentsTag.find(childrenTag, attrs=childrenTagAttrs))

def extract_children_tag_attrs_from_parents_tag(parentsTag, childrenTag, targetAttrs, childrenTagAttrs={}, ParentsIsMultiple=False, childIsMultiple=False):
        return [
                extract_attrs_from_tag(
                    extract_children_tag_from_parents_tag(parents, childrenTag),
                    targetAttrs
                )
                for parents \
                in parentsTag
            ] \
            if ParentsIsMultiple \
            else [
                extract_attrs_from_tag(kids, targetAttrs) \
                for kids \
                in extract_children_tag_from_parents_tag(parentsTag, childrenTag, childrenTagAttrs)
            ] 
            
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

def extract_emails(in_str):
    mail_list = re.findall(r'([a-zA-Z0-9-\.]+@[a-zA-Z0-9-]+.+[a-zA-Z0-9-]{2,4})', in_str)
    return mail_list

def extract_contact_numbers(in_str):
    contact_no_list = re.findall(r'(\d{2,3}[- .]?\d{3,4}[- .]?\d{4})', in_str)
    return contact_no_list