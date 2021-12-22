from bs4 import BeautifulSoup as bs
from jsonpath_ng import parse as jsonpath_parse
from datetime import datetime
import ast
import json
import xmltodict
import re
from w3lib.html import remove_tags

childIsNotMultiple = False
childIsMultiple = True
dataIsUnique = 'solo'
isNotRecursive = False
isMultiple = True
dummyAttrs = {}

def change_to_soup(reponseText):
    try :
        return bs(reponseText, 'html.parser')
    except UnboundLocalError as e :
        return remove_tags(reponseText)

def select_one(soup, tag):
    return soup.select_one(tag)

def extract_text(tag, isMultiple=False):
    try :
        return [clean_text(_.text) for _ in tag] if isMultiple else clean_text(tag.text)
    except AttributeError as e :
        print(e)
        return ''

def extract_contents(tag, isMultiple=False):
    return [_.contents for _ in tag] if isMultiple else tag.contents

def extract_attrs(tag, attrsName, isMultiple=False):
    return [_[attrsName] for _ in tag] if isMultiple else tag[attrsName]

def extract_children_tag(parentsTag, childrenTag, childrenTagAttrs={}, childIsMultiple=False, Recursive=True):
    return parentsTag.find_all(childrenTag, attrs=childrenTagAttrs, recursive=Recursive) \
        if childIsMultiple \
        else parentsTag.find(childrenTag, attrs=childrenTagAttrs, recursive=Recursive)

def find_next_tag(tag):
    return tag.find_next_siblings()[0]

def find_parent_tag(tag):
    return tag.parent

def decompose_tag(parentsTag, childrenTag, attrs):
    # 유일한 attrs 를 가지는 자식 태그 삭제 기능
    targetTag = parentsTag.find(childrenTag, attrs)
    targetTag.decompose()
    return parentsTag

def check_has_attrs_in_tag(tag, attrs):
    return tag.has_attr(attrs)
            
def check_children_tag_existence(parentsTag, childrenTag, childrenTagAttrs={}):
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
    specialWord = re.sub(r'[^\.|\-|\:|\/]', '', datetimeString)
    specialWordCount = {word:specialWord.count(word) for word in specialWord}
    if not specialWordCount and len(datetimeString) == 8:
        # 20210101처럼 구분 특수문자가 없는 형식일 경우
        year, month, days = datetimeString[:4], datetimeString[4:6], datetimeString[6:]
        datetimeString = year + "-" + month + "-" + days
        strptimeFormat = "%Y-%m-%d"
    else :
        # 2021-02-14 와 같이 구분자로 특수문자가 사용된 경우
        timeFormat = ['%Y{}%m{}%d ', '%H{}%M{}%S ']
        strptimeFormat = ''
        for idx, key in enumerate(specialWordCount):      
            if idx == 1 and len(datetimeString.split(' ')) == 2:
                if '24' in datetimeString.split(' ')[1] :
                    cleanedDate = " 00" + ''.join([':00' for _ in range(specialWordCount[key])])
                    datetimeString = datetimeString.split(' ')[0] + cleanedDate
            if specialWordCount[key] == 2 :
                strptimeFormat += timeFormat[idx].format(key, key)
            elif idx == 1 and specialWordCount[key] == 1:
                strptimeFormat += '%H{}%M '.format(key)
    try :
        time = datetime.strptime(datetimeString, strptimeFormat.strip()).isoformat()
    except ValueError:
        strptimeFormat = strptimeFormat.replace(strptimeFormat[1], strptimeFormat[1].lower())
        time = datetime.strptime(datetimeString, strptimeFormat.strip()).isoformat()
    return time

def convert_datetime_to_isoformat(date):
    return date.isoformat()

def extract_numbers_in_text(text):
    num = re.sub('[^0-9]', '', text)
    try :
        return int(num)
    except Exception as e :
        print(num)
        return 0

def extract_korean_in_text(text):
    return ' '.join(re.compile('[가-힣]+').findall(text))

def erase_html_tags(text):
    return re.sub('(<([^>]+)>)', '', text)

def extract_groupCode(text):
    return '_'.join(text.split('_')[:-1])

def convert_multiple_empty_erea_to_one_erea(text):
    return re.sub('\s+', ' ', text).strip()

def clean_text(text):
    try :
        eraseSpace = ['\r', '&lsquo;', '&rsquo;', '\u200b']
        leaveSpace = ['\xa0', '\n', '\t', '&nbsp;']
        for _ in eraseSpace:
            text = text.replace(_, '')
        for _ in leaveSpace:
            text = text.replace(_, ' ')
        text = convert_multiple_empty_erea_to_one_erea(text)
        return text
    except :
        return ''

def convert_response_contents_to_dict(contents):
    return xmltodict.parse(contents)

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
    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
    match = re.search(pattern, in_str)
    if match:
        return [match.group()]
    else :
        return []

def extract_contact_numbers_from_text(in_str):
    contact_no_list = re.findall(r'(\d{2,3}[- .]?\d{3,4}[- .]?\d{4})', in_str)
    return contact_no_list

def add_empty_list(local_var, keyList):
    for key in keyList:
        local_var[key] = []
    return local_var

def convert_merged_list_to_dict(keyList, valueList):
    result = {}
    for idx, key in enumerate(keyList):
        result.update({key : valueList[idx]})
    return result

def check_date_range_availability(dateRange, date):
    try :
        convertedDate = convert_datetime_string_to_isoformat_datetime(date)
    except ValueError :
        convertedDate = date
    startDate = dateRange[0]
    endDate = dateRange[1]
    if endDate <= convertedDate <= startDate:
        return 'vaild'
    else :
        return 'not valid'

def parse_onclick(text, order = 1):
    return re.findall("'(.+?)'", text)[order]

def convert_text_to_tuple(text):
    return ast.literal_eval(str(text))

def extract_values_list_in_both_sides_bracket_text(text):
    startIdx = text.find('(')
    endIdx = text.rfind(')')
    text = text[startIdx+1 : endIdx]
    valueList = [i.replace("'", "") for i in text.split(',')]
    return valueList

def multiple_appends(valueList, *element):
    valueList.extend(element)
    return valueList

def merge_var_to_dict(keyList, valueList, channelCode=''):
    lenthList = [len(_) for _ in valueList]
    if len(list(set(lenthList))) == 1:
        pass
    else :
        print(f'{channelCode} 채널 데이터 수집 에러')
        print({i : len(k) for i, k in zip(keyList, valueList)})
        return []
    result = []
    for idx in range(len(valueList[0])):
        result.append(
                {
                key: valueList[key_idx][idx] for key_idx, key in enumerate(keyList)
            }
        )
    return result

def extract_groupCode(text):
    # text = main_site__youthcenter_0
    return text.split('__')[0]

def extract_roomName_and_channelCode(text):
    # text = main_site__youthcenter_0
    channelCode = text.split('__')[1]
    roomName = channelCode.split('_')[0]
    return roomName, channelCode


def reflect_params(var, params):
    for key in params:
        var[key] = params[key]
    return var

def reflect_key(var, targetKeyInfo):
    keyList = []
    for Type in targetKeyInfo.keys():
        for key in targetKeyInfo[Type]:
            keyList.append(key)
            if Type == 'multipleType':
                var[key] = []
            elif Type == 'singleType':
                var[key] = ''
    return var, keyList


def html_type_default_setting(params, targetKeyInfo):
    var = reflect_params(locals(), params)
    var, keyList = reflect_key(var, targetKeyInfo)
    text = var['response'].text
    soup = change_to_soup(
        text
    )
    return var, soup, keyList, text

def json_type_default_setting(params, targetKeyInfo):
    var = reflect_params(locals(), params)
    var, keyList = reflect_key(var, targetKeyInfo)
    jsonData = json.loads(var['response'].text)
    return var, jsonData, keyList

def extract_text_between_prefix_and_suffix(prefix, suffix, text):
    return text[text.find(prefix)+len(prefix):text.find(suffix)]

def search_img_list_in_contents(contents, channelMainUrl):
    imgList = extract_children_tag(contents, 'img', {'src' : True}, childIsMultiple)
    imgs = []
    if imgList:
        for img in imgList:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = channelMainUrl + src
            imgs.append(src)
    return imgs