from bs4 import BeautifulSoup as bs
from jsonpath_ng import parse as jsonpath_parse
from datetime import datetime
import ast
import json
import xmltodict
import re
from w3lib.html import remove_tags
from urllib.parse import urljoin


class DataStatus():
    not_multiple = False
    multiple = True
    unique = 'solo'
    not_recursive = False
    empty_attrs = {}

def change_to_soup(reponse_text):
    try :
        return bs(reponse_text, 'html.parser')
    except UnboundLocalError as e :
        return remove_tags(reponse_text)

def extract_text(tag, is_multiple=False):
    try :
        return [clean_text(_.text) for _ in tag] if is_multiple else clean_text(tag.text)
    except AttributeError as e :
        print(e, '\n', tag)
        return ''

def extract_contents(tag, is_multiple=False):
    return [_.contents for _ in tag] if is_multiple else tag.contents

def extract_attrs(tag, attrs_name, is_multiple=False):
    return [_[attrs_name] for _ in tag] if is_multiple else tag[attrs_name]

def extract_children_tag(parents_tag, children_tag, children_tag_attrs={}, child_is_multiple=False, Recursive=True):
    return parents_tag.find_all(children_tag, attrs=children_tag_attrs, recursive=Recursive) \
        if DataStatus.multiple is child_is_multiple \
        else parents_tag.find(children_tag, attrs=children_tag_attrs, recursive=Recursive)

def find_next_tag(tag):
    return tag.find_next_siblings()[0]

def find_parent_tag(tag):
    return tag.parent

def decompose_tag(parents_tag, children_tag, attrs, multiple=False):
    # 유일한 attrs 를 가지는 자식 태그 삭제 기능
    if multiple:
        target_tag = parents_tag.find_all(children_tag, attrs)
        if target_tag:
            for tag in target_tag:
                tag.decompose()
    else :
        target_tag = parents_tag.find(children_tag, attrs)
        target_tag.decompose()
    return parents_tag

def split_value_list_based_on_key(key_list, value_list):
    return {
        {key : value_list[keyIdx]} \
        for keyIdx, key \
        in enumerate(key_list)
    }

def convert_datetime_string_to_isoformat_datetime(datetime_string):
    special_word = re.sub(r'[^\.|\-|\:|\/]', '', datetime_string)
    special_word_count = {word:special_word.count(word) for word in special_word}
    if not special_word_count and len(datetime_string) == 8:
        # 20210101처럼 구분 특수문자가 없는 형식일 경우
        year, month, days = datetime_string[:4], datetime_string[4:6], datetime_string[6:]
        datetime_string = year + "-" + month + "-" + days
        strptime_format = "%Y-%m-%d"
    else :
        # 2021-02-14 와 같이 구분자로 특수문자가 사용된 경우
        timeFormat = ['%Y{}%m{}%d ', '%H{}%M{}%S ']
        strptime_format = ''
        for idx, key in enumerate(special_word_count):      
            if idx == 1 and len(datetime_string.split(' ')) == 2:
                if '24' in datetime_string.split(' ')[1] :
                    cleanedDate = " 00" + ''.join([':00' for _ in range(special_word_count[key])])
                    datetime_string = datetime_string.split(' ')[0] + cleanedDate
            if special_word_count[key] == 2 :
                strptime_format += timeFormat[idx].format(key, key)
            elif idx == 1 and special_word_count[key] == 1:
                strptime_format += '%H{}%M '.format(key)
    try :
        time = datetime.strptime(datetime_string, strptime_format.strip()).isoformat()
    except ValueError:
        strptime_format = strptime_format.replace(strptime_format[1], strptime_format[1].lower())
        time = datetime.strptime(datetime_string, strptime_format.strip()).isoformat()
    return time

def convert_datetime_to_isoformat(date):
    return date.isoformat()

def extract_numbers_in_text(text):
    num = re.sub('[^0-9]', '', text)
    return int(num)

def extract_korean_in_text(text):
    return ' '.join(re.compile('[가-힣]+').findall(text))

def erase_html_tags(text):
    return re.sub('(<([^>]+)>)', '', text)

def extract_group_code(text):
    return '_'.join(text.split('_')[:-1])

def convert_multiple_empty_erea_to_one_erea(text):
    return re.sub('\s+', ' ', text).strip()

def clean_text(text):
    try :
        erase_space = ['\r', '&lsquo;', '&rsquo;', '\u200b']
        leave_space = ['\xa0', '\n', '\t', '&nbsp;']
        for _ in erase_space:
            text = text.replace(_, '')
        for _ in leave_space:
            text = text.replace(_, ' ')
        text = convert_multiple_empty_erea_to_one_erea(text)
        return text
    except :
        return ''

def convert_response_contents_to_dict(contents):
    return xmltodict.parse(contents)

def search_value_in_json_data_using_path(json_data, path, number_of_data='multiple', reverse = False):
    tartget_data = jsonpath_parse(path).find(json_data)
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

def add_empty_list(local_var, key_list):
    for key in key_list:
        local_var[key] = []
    return local_var

def convert_merged_list_to_dict(key_list, value_list):
    result = {}
    for idx, key in enumerate(key_list):
        result.update({key : value_list[idx]})
    return result

def check_date_range_availability(date_range, date):
    try :
        converted_date = convert_datetime_string_to_isoformat_datetime(date)
    except ValueError :
        converted_date = date
    start_date = date_range[0]
    end_date = date_range[1]
    if end_date <= converted_date <= start_date:
        return 'vaild'
    else :
        return 'not valid'

def parse_onclick(text, order = 1):
    return re.findall("'(.+?)'", text)[order]

def convert_text_to_tuple(text):
    return ast.literal_eval(str(text))

def extract_text_from_single_tag(soup, tag, attrs):
    tag = extract_children_tag(soup, tag, attrs, DataStatus.not_multiple)
    text = extract_text(tag)
    return text

def extract_attrs_from_single_tag(soup, tag, attrs, targetAttrs):
    tag = extract_children_tag(soup, tag, attrs, DataStatus.not_multiple)
    attrs = extract_attrs(tag, targetAttrs)
    return attrs

def extract_values_list_in_both_sides_bracket_text(text):
    start_idx = text.find('(')
    end_idx = text.rfind(')')
    text = text[start_idx+1 : end_idx]
    value_list = [i.replace("'", "") for i in text.split(',')]
    return value_list

def multiple_appends(value_list, *element):
    value_list.extend(element)
    return value_list

def merge_var_to_dict(key_list, value_list, channel_code=''):
    lenth_list = [len(_) for _ in value_list]
    if len(list(set(lenth_list))) == 1:
        pass
    else :
        print(f'{channel_code} 채널 데이터 수집 에러')
        print({i : len(k) for i, k in zip(key_list, value_list)})
        return []
    result = []
    for idx in range(len(value_list[0])):
        result.append(
                {
                key: value_list[key_idx][idx] for key_idx, key in enumerate(key_list)
            }
        )
    return result

def extract_group_code(text):
    # text = main_site__youthcenter_0
    return text.split('__')[0]

def extract_room_name_and_channel_code(text):
    # text = main_site__youthcenter_0
    channel_code = text.split('__')[1]
    room_name = channel_code.split('_')[0]
    return room_name, channel_code

def reflect_params(var, params):
    for key in params:
        var[key] = params[key]
    return var

def reflect_key(var, target_key_info):
    key_list = []
    for Type in target_key_info.keys():
        for key in target_key_info[Type]:
            key_list.append(key)
            if Type == 'multiple_type':
                var[key] = []
            elif Type == 'single_type':
                var[key] = ''
    return var, key_list

def html_type_default_setting(params, target_key_info):
    var = reflect_params(locals(), params)
    var, key_list = reflect_key(var, target_key_info)
    # text = var['response'].text
    text = var['response'].content.decode('utf-8','replace')
    soup = change_to_soup(
        text
    )
    return var, soup, key_list, text

def json_type_default_setting(params, target_key_info):
    var = reflect_params(locals(), params)
    var, key_list = reflect_key(var, target_key_info)
    json_data = json.loads(var['response'].text)
    return var, json_data, key_list

def extract_text_between_prefix_and_suffix(prefix, suffix, text):
    return text[text.find(prefix)+len(prefix):text.find(suffix)]


def search_img_list_in_contents(contents, channel_main_url):
    img_list = extract_children_tag(contents, 'img', {'src' : True}, DataStatus.multiple)
    imgs = []
    if img_list:
        for img in img_list:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = urljoin(channel_main_url, src)
            imgs.append(src)
    return imgs


def make_absolute_img_src(img_src, channel_main_url):
    """
    img 태그의 src가 상대 경로인 경우 절대경로로 변환
    :param img_src: img 태그의 src
    :param channel_main_url: host
    :return: 이미지 절대경로 or base64 인코딩 파일
    """
    if 'http' in img_src or 'base64' in img_src:
        return img_src

    return urljoin(channel_main_url, img_src)


def make_absolute_url(in_url, channel_main_url):
    """
    url이 상대경로이면 절대로 변환하여 리턴, 절대 경로이면 그대로 리턴
    :param in_url: 변환 대상 url
    :param channel_main_url: host
    :return: url의 절대경로
    """
    if 'http' in in_url:
        return in_url

    return urljoin(channel_main_url, in_url)
