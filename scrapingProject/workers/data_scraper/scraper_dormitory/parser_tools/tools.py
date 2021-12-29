from bs4 import BeautifulSoup as bs
from jsonpath_ng import parse as jsonpath_parse
from datetime import datetime
import ast
import json
import re
from w3lib.html import remove_tags

def change_to_soup(reponse_text):
    # response.text 를 soup로 변환
    try :
        soup = bs(reponse_text, 'html.parser')
        return soup
    except UnboundLocalError as e :
        # parser.py soup 변수에 Tag가 삭제된 response.text 를 반환함
        return remove_tags(reponse_text)

def extract_text(tag, is_child_multiple=False):
    # Tag 내의 Text를 반환함
    if is_child_multiple:
        tag_list = tag
        text_list = [clean_text(tag.text) for tag in tag_list]
        return text_list
    else :
        text = clean_text(tag.text)
        return text

def extract_attrs(tag, attrs_name, is_child_multiple=False):
    # Tag의 Attrs를 반환함
    if is_child_multiple:
        tag_list = tag
        attrs_list = [tag[attrs_name] for tag in tag_list]
        return attrs_list
    else :
        return tag[attrs_name]

def extract_children_tag(parents_tag, child_tag, child_tag_attrs={}, is_child_multiple=False, is_recursive=True):
    # 자식 태그의 attrs 가 없고, 개수가 1개인 설정이 기본값
    # bs4.Tag 를 반환함
    # 여러개의 자식태그를 찾고 싶다면 
    # is_child_multiple=True 로 선언
    # 결과는 bs4.Tag 가 아닌 bs4.tag List 를 반환
    if is_child_multiple :
        child_tag_list = parents_tag.find_all(child_tag, attrs=child_tag_attrs, recursive=is_recursive)
        return child_tag_list
    else :
        child_tag = parents_tag.find(child_tag, attrs=child_tag_attrs, recursive=is_recursive)
        return child_tag

def find_next_tag(tag):
    # 기준 Tag 다음 위치에 등장하는 Tag를 반환함
    next_tag = tag.find_next_siblings()[0]
    return next_tag
    
def find_parent_tag(tag):
    # 부모 Tag를 반환함
    parent_tag = tag.parent
    return parent_tag

def decompose_tag(parents_tag, child_tag, child_tag_attrs, is_child_multiple=False):
    # child tag를 삭제한 parent tag를 반환함
    if is_child_multiple:
        target_tag_list = parents_tag.find_all(child_tag, child_tag_attrs)
        if target_tag_list:
            for tag in target_tag_list:
                tag.decompose()
    else :
        target_tag = parents_tag.find(child_tag, child_tag_attrs)
        target_tag.decompose()
    return parents_tag

def convert_datetime_string_to_isoformat_datetime(datetime_string):
    # 날짜 텍스트를 isoformat datetime으로 반환함
    special_word = re.sub(r'[^\.|\-|\:|\/]', '', datetime_string)
    special_word_count = {word:special_word.count(word) for word in special_word}
    if not special_word_count and len(datetime_string) == 8:
        # 20210101처럼 구분 특수문자가 없는 날짜 형식일 경우
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

def extract_numbers_in_text(text):
    # 텍스트에서 숫자만 추출해서 숫자를 반환
    num = re.sub('[^0-9]', '', text)
    return int(num)

def erase_html_tags(text):
    # 텍스트에서 html 태그를 제거하고 텍스트를 반환
    return re.sub('(<([^>]+)>)', '', text)

def clean_text(text):
    try :
        erase_space = ['\r', '&lsquo;', '&rsquo;', '\u200b']
        leave_space = ['\xa0', '\n', '\t', '&nbsp;']
        for _ in erase_space:
            text = text.replace(_, '')
        for _ in leave_space:
            text = text.replace(_, ' ')
        text = re.sub('\s+', ' ', text).strip()
        return text
    except :
        return ''

def search_value_in_json_data_using_path(json_data, path, is_data_multiple=True, find_from_the_end=False):
    tartget_data = jsonpath_parse(path).find(json_data)
    result = []
    if tartget_data and not is_data_multiple:
        result = tartget_data[0].value
        if find_from_the_end :
            result = tartget_data[-1].value
    elif tartget_data and is_data_multiple:
        result = [_.value for _ in tartget_data]
    return result

def extract_emails(in_str):
    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
    match = re.search(pattern, in_str)
    if match:
        return [match.group()]
    else :
        return []

def extract_contact_numbers_from_text(in_str):
    # 텍스트에서 연락처를 찾아 list로 반환
    contact_no_list = re.findall(r'(\d{2,3}[- .]?\d{3,4}[- .]?\d{4})', in_str)
    return contact_no_list

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

def parse_onclick(text, idx=1):
    return re.findall("'(.+?)'", text)[idx]

def convert_text_to_tuple(text):
    return ast.literal_eval(str(text))

def extract_text_from_single_tag(soup, tag, attrs):
    tag = extract_children_tag(soup, tag, attrs, is_child_multiple=False)
    text = extract_text(tag)
    return text

def extract_values_list_in_both_sides_bracket_text(text):
    start_idx = text.find('(')
    end_idx = text.rfind(')')
    text = text[start_idx+1 : end_idx]
    value_list = [i.replace("'", "") for i in text.split(',')]
    return value_list

def merge_var_to_dict(key_list, value_list, channel_code=''):
    # parser.py에서 포스트에 대한 정보를 key:value 꼴로 맵핑하는 기능
    # 수집된 데이터의 개수가 상이할 경우 빈 리스트를 반환하고 해당 데이터별 개수를 print 함 
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
    # scraping_manager.py 에서 폴더 경로를 찾기위한 기능의 일부
    group_code = text.split('__')[0]
    return group_code

def extract_room_name_and_channel_code(text):
    # text = main_site__youthcenter_0
    # scraping_manager.py 에서 폴더 경로를 찾기위한 기능의 일부
    channel_code = text.split('__')[1]
    room_name = channel_code.split('_')[0]
    return room_name, channel_code

def reflect_params(var, params):
    for key in params:
        var[key] = params[key]
    return var

def reflect_key(var, target_key_info):
    # 데이터를 담을 빈 리스트 혹은 공백 문자열을 만드는 기능
    # 더미 데이터와 key list 를 함께 반환
    '''
        target_key_info = {
            'single_type' : ['post_text', 'post_title', 'contact'],
            'multiple_type' : ['post_image_url']
        }
        인 경우 
        var['post_text'] = ''
        var['post_title'] = ''
        var['contact'] = ''
        var['post_image_url'] = []
        를 var 에 포함시킴
    '''
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
    # 데이터가 제공되는 방식이 html인 경우에 사용함
    # 해당 요청 데이터에서 어떤 key값을 찾을지를 넘겨받아
    # 해당 key 값의 더미데이터 형식을 var 에 담아 반환함
    # soup 는 BeautifulSoup 객체
    # key_list 는 수집할 대상이 될 key list 
    # text 의 경우 response.text 를 그대로 반환하며, 
    # BeautifulSoup 객체에서 데이터를 파싱할 수 없을 경우 사용함
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
    # 주로 post_url 구성시 post_id 를 찾기위해서 href를 parsing할 경우에 사용함
    # text 에서 prefix 문자와 suffix 문자 사이의 값을 반환함
    return text[text.find(prefix)+len(prefix):text.find(suffix)]

def search_img_list_in_contents(contents, channel_main_url):
    # 흔히 사용되는 이미지 리스트 추출 로직
    # 포스트 내용('post_text')이 담긴 tag 내부에서 img tag를 찾아서 반환함
    # channle의 url이 포함되지 않은 src Attrs 인 경우 
    # channel_main_url + src 로 반영함
    img_list = extract_children_tag(contents, 'img', {'src' : True}, is_child_multiple=True)
    imgs = []
    if img_list:
        for img in img_list:
            src = extract_attrs(img, 'src')
            if 'http' not in src and 'base64' not in src :
                src = channel_main_url + src
            imgs.append(src)
    return imgs