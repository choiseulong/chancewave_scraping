from bs4 import BeautifulSoup as bs
import bs4
from jsonpath_ng import parse as jsonpath_parse
from datetime import datetime
import ast
import json
import re
from pytz import timezone
from w3lib.html import remove_tags
from urllib.parse import urljoin


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
    if not isinstance(tag, bs4.element.Tag):
        return ''

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
        attrs_value = tag[attrs_name]
        if attrs_name == 'href' and attrs_value:
            attrs_value = parse_href_in_tools(attrs_value)
        return attrs_value

def parse_href_in_tools(attrs):
    if './' == attrs[:2]:
        attrs = attrs[1:]
    return attrs

def extract_children_tag(parents_tag, child_tag, child_tag_attrs={}, is_child_multiple=False, is_recursive=True):
    # 자식 태그의 attrs 가 없고, 개수가 1개인 설정이 기본값
    # bs4.Tag 를 반환함
    # 여러개의 자식태그를 찾고 싶다면
    # is_child_multiple=True 로 선언
    # 결과는 bs4.Tag 가 아닌 bs4.tag List 를 반환
    if parents_tag.find(child_tag, child_tag_attrs):
        if is_child_multiple :
            child_tag_list = parents_tag.find_all(child_tag, attrs=child_tag_attrs, recursive=is_recursive)
            return child_tag_list
        else :
            child_tag = parents_tag.find(child_tag, attrs=child_tag_attrs, recursive=is_recursive)
            return child_tag
    else :
        return

def find_next_tag(tag):
    # 기준 Tag 다음 위치에 등장하는 Tag를 반환함
    next_tag = tag.find_next_siblings()
    if next_tag :
        return next_tag[0]

def find_parent_tag(tag):
    # 부모 Tag를 반환함
    parent_tag = tag.parent
    return parent_tag

def decompose_tag(parents_tag, child_tag, child_tag_attrs={}, is_child_multiple=False):
    # child tag를 삭제한 parent tag를 반환함
    if is_child_multiple:
        target_tag_list = parents_tag.find_all(child_tag, child_tag_attrs)
        if target_tag_list:
            for tag in target_tag_list:
                tag.decompose()
    else :
        target_tag = parents_tag.find(child_tag, child_tag_attrs)
        if target_tag :
            target_tag.decompose()
    return parents_tag

def convert_datetime_string_to_isoformat_datetime(datetime_string):
    # 날짜 텍스트를 isoformat datetime으로 반환함
    special_word = re.sub(r'[^\.|\-|\:|\/]', '', datetime_string)
    special_word_count = {word:special_word.count(word) for word in special_word}
    if len(special_word_count) == 1 and ':' in special_word_count.keys():
        # 당일 업로드 되어 날짜가 아닌 시간:분:초로 제공될 경우.
        today = datetime.now(timezone('Asia/Seoul')).isoformat()
        return today
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
        erase_space = ['\r', '&lsquo;', '&rsquo;', '\u200b', '/ufeff', '\ufeff']
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
    result_list = []
    if type(path) == dict :
        for pas in path:
            result = search_value_in_json_data_using_path(json_data, pas)
            result_list.append(result)
        return result_list
    else :
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
    contact_list = []
    contact_no_list = re.findall(r'(\d{2,3}[- .]?\d{3,4}[- .]?\d{4})', in_str)
    contact_list = list(set(contact_no_list))
    if len(contact_list) == 1 :
        return contact_list[0]
    return contact_list

def convert_merged_list_to_dict(key_list, var):
    value_list = [var[key] for key in key_list]
    result = {}
    for idx, key in enumerate(key_list):
        result.update({key : value_list[idx]})
    return result

def parse_post_id(child_tag_text, idx=1):
    post_id_candidate = [param.strip() for param in extract_values_list_in_both_sides_bracket_text(child_tag_text) if param]
    result = [post_id_candidate[_] for _ in idx] if type(idx) == list else post_id_candidate[idx]
    return result

def convert_text_to_tuple(text):
    return ast.literal_eval(str(text))

def extract_text_from_single_tag(parent_tag, child_tag, child_tag_attrs={}):
    text = extract_text(
        extract_children_tag(parent_tag, child_tag, child_tag_attrs=child_tag_attrs, is_child_multiple=False)
    )
    return text

def extract_values_list_in_both_sides_bracket_text(text):
    text_cut = text[text.find('(')+1 : text.rfind(')')].replace("'", "").replace('"', '')
    value_list = [i for i in text_cut.split(',')]
    return value_list

def assign_multiple_table_data_to_key_name(value_list):
    lenth_list = [len(_) for _ in value_list]
    deduplication_lenth_list = list(set(lenth_list))
    if len(deduplication_lenth_list) == 2 :
        for data_idx, data_len in enumerate(lenth_list):
            if lenth_list.count(data_len) == 1 and data_len % 2 == 0:
                data_list = value_list[data_idx]
                half_data_length = int(len(data_list)/2)
                merged_data_list = []
                for idx in range(half_data_length):
                    merged_data_list.append(data_list[idx*2] + ' - ' + data_list[idx*2 + 1])
                value_list[data_idx] = merged_data_list
    return value_list

def merge_var_to_dict(key_list, var):
    # parser.py에서 포스트에 대한 정보를 key:value 꼴로 맵핑하는 기능
    # 수집된 데이터의 개수가 상이할 경우 빈 리스트를 반환하고 해당 데이터별 개수를 print 함 
    channel_code = var['channel_code']
    value_list = [var[key] for key in key_list]
    value_list = assign_multiple_table_data_to_key_name(value_list)
    value_lenth_list = [len(_) for _ in value_list]
    if len(list(set(value_lenth_list))) == 1:
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
    encoding = var['response'].encoding
    if encoding == 'ISO-8859-1':
        encoding = 'EUC-KR'
    if type(encoding) == type(None):
        encoding = 'UTF-8'

    text = var['response'].content.decode(encoding,'replace')
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
    # return text[text.find(prefix)+len(prefix):text.find(suffix)]
    truncated_front_part_text = text[text.find(prefix)+len(prefix):]
    truncated_text = truncated_front_part_text[:truncated_front_part_text.find(suffix)]
    return truncated_text


def search_img_list_in_contents(contents, channel_main_url):
    # 흔히 사용되는 이미지 리스트 추출 로직
    # 포스트 내용('post_text')이 담긴 tag 내부에서 img tag를 찾아서 반환함
    # channle의 url이 포함되지 않은 src Attrs 인 경우
    # channel_main_url + src 로 반영함
    if not contents :
        print(f'{channel_main_url} contents is empty')
        return
    img_list = extract_children_tag(contents, 'img', {'src' : True}, is_child_multiple=True)
    imgs = []
    if img_list:
        for img in img_list:
            src = extract_attrs(img, 'src')
            if src.startswith('./'):
                src = src[1:]
            elif src.startswith('../'):
                src = src[2:]
            elif src.startswith('file:///'):
                continue

            if src.startswith('//www.'):
                src = src[2:]
                imgs.append(src)
                continue
            if 'http' not in src and 'base64' not in src :
                src = urljoin(channel_main_url, src)
            imgs.append(src)
    return imgs

def _map_key_name_with_table_header(**kargs):
    # 게시물 리스트 스크래핑 진행시 테이블 헤더로 제공되는 항목
    # api key값과 맵핑함
    var = kargs['var']
    input_table_header = var['table_header']
    included_key_info = {}
    header_info = {
        'post_url' : ["제목", "행사명", "강좌명", "제 목", "글제목", "강좌명", "서비스명",\
             "강좌명/교육기관", "공모·모집명"],
        'post_title' : ["제목", "행사명", "강좌명", "제 목", "글제목", "강좌명", "서비스명",\
             "강좌명/교육기관", "공모·모집명"],
        'uploaded_time' : ["작성일", "등록일", "게시일", "등록일자", "일자", "작성일자", "날짜",\
             "공고일", "입력일"],
        'view_count' : ["조회", "조회수"],
        'uploader' : ["작성자", "담당부서", "게시자", "등록자", "부서", "담당자", "작성부서", "기관",\
             "제공기관", "부서명", "글쓴이", "추진부서"],
        'post_subject' : ["분류", "구분", "분야", "서비스유형"],
        'contact' : ["연락처"],
        'is_going_on' : ["접수상태", "상태", "공모상태"],
        'post_content_target' : ["대상자", "대상"],
        'linked_post_url' : ["바로가기"]
    }
    for header_idx, header_name in enumerate(input_table_header):
        for key_name in header_info:
            if header_name in header_info[key_name]:
                if header_idx not in included_key_info.keys():
                    included_key_info.update({header_idx : []})
                included_key_info[header_idx].append(key_name)
    var['included_key_info'] = included_key_info
    return var

def _check_valid_key(**kargs):
    # key_list = ['uploaded_time', 'view_count', 'uploader', 'post_url']
    # included_key_info = {1: ['post_url', 'post_title'], 2: ['uploaded_time'], 3: ['view_count']}
    # result = {1: ['post_url'], 2: ['uploaded_time'], 3: ['view_count']}
    var, key_list = kargs['var'], kargs['key_list']
    included_key_info = var['included_key_info']
    result = {}
    for idx in included_key_info:
        for key_name in included_key_info[idx]:
            if key_name in key_list:
                if idx not in result.keys():
                    result.update({idx:[]})
                result[idx].append(key_name)
    var['checked_key_info'] = result
    return var

def _search_table_header_list(**kargs):
    soup, var = kargs['soup'], kargs['var']
    thead = extract_children_tag(soup, 'thead')
    tabel_header_box = var['table_header_box'] if 'table_header_box' in var.keys() else extract_children_tag(thead, 'tr')
    print(var['table_header_box'])
    var['page_table_header'] = [
        extract_text(child) \
        for child \
        in tabel_header_box.children\
        if extract_text(child)
    ]
    return var

def _compare_input_header_with_table_header(**kargs):
    var = kargs['var']
    input_table_header = var['table_header']
    page_tabel_header = var['page_table_header']
    if input_table_header != page_tabel_header:
        if var['dev'] :
            print(f'Table Header Warning\nCHANNEL_URL : {var["channel_url"]}')
            print(f'Input Table Header : {input_table_header}\nPage Table Header : {page_tabel_header}')
            if len(input_table_header) != len(input_table_header):
                print(f'TABLE LENGTH DID NOT MATCH\nInput Table Header : {len(input_table_header)}\nPage Table Header : {len(page_tabel_header)}')
            else :
                for table_idx in range(len(input_table_header)):
                    try :
                        if input_table_header[table_idx] != page_tabel_header[table_idx]:
                            print(
                                f'HEADER NAME DID NOT MATCH INDEX : {table_idx}\
                                \nInput Table Header : {input_table_header[table_idx]}\
                                \nPage Table Header : {page_tabel_header[table_idx]}'
                            )
                    except IndexError:
                        # TypeError: exceptions must derive from BaseException
                        raise(
                            'TABLE HEADER LENGTH DID NOT MATCH'
                        )
        else :
            print(f'Table Header Warning\n{var["channel_main_url"]}')
    else :
        if var['dev'] :
            print('header pass')
    return var

def _check_table_data_validation(var):
    table_header_length = len(var['table_header']) # parser.py 에서 선언한 테이블 헤더
    table_data_list = var['table_data_list'] # 부모 태그의 자식 태그 리스트
    valid_child_tag_list = [] # 옳바른 자식을 담을 빈 리스트
    for child_tag_idx, child_tag in enumerate(table_data_list):
        seed_tag = _seperate_parents_tag_to_child_tag_list(child_tag) # 자식태그의 seed 태그 리스트
        if len(seed_tag) == table_header_length: # 헤더 길이와 일치하다면
            valid_child_tag_list.append(table_data_list[child_tag_idx]) # 옳바른 자식으로 편입
    var['table_data_list'] = valid_child_tag_list # 부모 태그 내 옳바른 자식 태그 리스트
    return var

def _search_table_data_list(**kargs):
    soup, var = kargs['soup'], kargs['var']
    if 'table_data_box' in var.keys():
        table_data_box = var['table_data_box']
    else :
        table_data_box = extract_children_tag(soup, 'tbody', is_child_multiple=True)
        if len(table_data_box) == 1 :
            table_data_box = table_data_box[0]
        else :
            table_data_box = table_data_box[1]
        table_data_box = _handle_tbody_exception(soup, tbody=table_data_box)
    var['table_data_list'] = _seperate_parents_tag_to_child_tag_list(table_data_box)
    var = _check_table_data_validation(var)
    if not var['table_data_list'] :
        var['table_data_list'] = 'break'
    return var

def _handle_tbody_exception(soup, tbody):
    # tbody가 2개 등장하는데 첫 번째 tbody 가 공백인 예외 처리
    tbody_list = extract_children_tag(soup, 'tbody', is_child_multiple=True)
    if len(tbody_list) > 1 and not tbody.text:
        tbody = tbody_list[1]
    return tbody

def parse_is_going_on(**params):
    text = params['child_tag_text']
    on_progress = ['진행', '모집중', '접수대기', '접수중', '교육중']
    dead = ['마감', '교육완료', '접수마감']
    result = None
    for word in on_progress:
        if word in text :
            result = True
    
    for word in dead:
        if word in text :
            if type(result) == type(None):
                result = False
            else :
                return 'ERROR'
    # print(var['channel_code'], 'IS_GOING_ON PARSER VALUE DUPLICATE ERROR')
    return result

def parse_uploaded_time(**params):
    # 기본 등록일 처리.
    # 예외 케이스로 등록일을 처리할 경우 직접 작성
    # parse_view_count 를 작성해서 처리하거나 포스트 개별 페이지 파싱에서 처리함
    text = params['child_tag_text'].replace(' ', '')
    if text.endswith('.'):
        text = text[:-1]
    
    result = convert_datetime_string_to_isoformat_datetime(text)
    return result

def parse_view_count(**params):
    # 기본 조회수 처리.
    # parse_view_count 를 작성해서 처리하거나 포스트 개별 페이지 파싱에서 처리함
    num = params['child_tag_text']
    result = extract_numbers_in_text(num)
    return result

def parse_href(href):
    if href.startswith('#'):
        href = href[1:]
    if href.startswith('../'):
        href = href[2:]
    return href

def parse_linked_post_url(**params):
    child_tag = params['child_tag']
    var = params['var']
    a_tag = extract_children_tag(child_tag, 'a')
    href = extract_attrs(a_tag, 'href') if a_tag.has_attr('href') else ''
    return href

def parse_post_url(**params):
    # 첫 번쩨 케이스
    # a태그 href 가 존재하고 self.post_url을 선언하지 않은 경우
    # var['channel_main_url'] + href 로 post_url 을 만들어서 return함

    # 두 번째 케이스
    # a태그 href 가 존재하고 self.post_url을 선언한 경우
    # var['post_url_frame'] 내에 '{}' 가 없을 경우
    # var['post_url_frame'] + href
    # var['post_url_frame'] 내에 '{}' 가 있을 경우
    # var['post_url_frame'].format(href) 로 post_url 을 구성해 return 함

    # 세 번째 케이스
    # var['post_id_idx'] int 값이 존재하고 self.post_url 이 선언된 경우
    # 해당 index의 onclick 파싱값(post_id)을 var['post_url_frame'].format(post_id)로
    # post_url을 사용해 return 함

    # 네 번째 케이스
    # var['post_id_idx'] list 값이 존재하고 self.post_url 이 선언된 경우
    # var['post_url_frame'].replace('{}', 순차적으로 추출한 post_id, 1)
    # 으로 url 을 만들어 return 함 onclick에 제시되는 파라미터 순으로 url 정렬이 필요할수도 있음.
    # 손이 많이가는 경우라면 직접 parse_ 를 작성해서 사용
    child_tag = params['child_tag']
    var = params['var']
    post_url_frame = var['post_url_frame']
    a_tag = extract_children_tag(child_tag, 'a')
    href = extract_attrs(a_tag, 'href') if a_tag.has_attr('href') else ''
    if href :
        href = parse_href(href)
    onclick = extract_attrs(a_tag, 'onclick') if a_tag.has_attr('onclick') else ''
    if 'post_id_idx' in var.keys() :
        if type(var['post_id_idx']) == int:
            if onclick :
                post_id = parse_post_id(onclick, var['post_id_idx'])
            elif href :
                post_id = parse_post_id(href, var['post_id_idx'])
            result = post_url_frame.format(post_id)
            return result
        elif type(var['post_id_idx']) == list:
            if onclick :
                post_id_list = parse_post_id(onclick, var['post_id_idx'])
            elif href :
                post_id_list = parse_post_id(href, var['post_id_idx'])
            for post_id in post_id_list:
                post_url_frame = post_url_frame.replace('{}', post_id, 1)
            result = post_url_frame
            return result
    else :
        if post_url_frame:
            if '{}' in post_url_frame:
                result = post_url_frame.format(href)
            else :
                result = post_url_frame + href
            return result
        else :
            result = var['channel_main_url'] + href
            return result

def parse_post_title(**params):
    child_tag = params['child_tag']
    var = params['var']
    a_tag = extract_children_tag(child_tag, 'a')
    text = extract_text(a_tag)
    if '...' in params['child_tag_text']:
        if a_tag.has_attr('title'):
            text = extract_attrs(a_tag, 'title')
            return text
        else :
            print(var['channel_code'], 'post_title error')
            return None
    else :
        return text

def _return_raw_text(**params):
    return params['child_tag_text']

parse_contact = parse_post_subject = parse_uploader = parse_post_content_target\
     = _return_raw_text
    
def _check_notice_post(child_tag_text, page_count):
    # text -> child_tag_text[0]
    # 공지글 첫 페이지에서만 수집을 위함
    if '공지' in child_tag_text or not child_tag_text:
        if page_count != 1:
            return True
    return False


def _seperate_parents_tag_to_child_tag_list(parents_tag):
    child_tag_list = [child for child in parents_tag.children if isinstance(child, bs4.element.Tag)]
    return child_tag_list


def _parse_total_table_data(**kargs):
    var = kargs['var']
    checked_key_info, table_data_list = var['checked_key_info'], var['table_data_list']
    if var['table_data_list'] == 'break':
        return var
    for table_data in table_data_list :
        table_data_text = extract_text(table_data)
        if '등록된 글이 없습니다' == table_data_text:
            var['table_data_list'] = 'break'
            return var
        # 입력한 header 순번에 맞춰 해당 값을 파싱하는 함수에 전달함
        child_tag_list = _seperate_parents_tag_to_child_tag_list(table_data)
        child_tag_text_list = [extract_text(child_tag) for child_tag in child_tag_list]
        is_notice = _check_notice_post(child_tag_text = child_tag_text_list[0], page_count=var['page_count'])
        if not is_notice : pass
        if '공지' in child_tag_text_list[0] or not child_tag_text_list[0]: # 공지글 첫 페이지에서만 수집
            if var['page_count'] != 1:
                continue
        for child_tag_idx in checked_key_info:
            for key_name in checked_key_info[child_tag_idx]:
                func_name = f'parse_{key_name}'
                if func_name in var.keys():
                    try :
                        var[key_name].append(
                            var[func_name](
                                var=var,
                                child_tag=child_tag_list[child_tag_idx], 
                                child_tag_text=child_tag_text_list[child_tag_idx],
                            )
                        )
                    except KeyError as e :
                        print(e)
                        print(func_name, '미선언')
                else :
                    globals()[func_name](var=var, child_tag_text=child_tag_text_list[child_tag_idx], child_tag=child_tag_list[child_tag_idx])
    return var


def _add_title_index_to_var(**kargs):
    var = kargs['var']
    checked_key_info = var['checked_key_info']
    for idx in checked_key_info:
        if 'post_title' in checked_key_info[idx]:
            var['title_idx'] = idx
            break
    return var


def parse_board_type_html_page(soup, var, key_list):
    # 테이블 헤더, 데이블 데이터가 리스트 형식으로 담긴 태그가 있을때 사용할 수 있음
    # var['table_data_box'] 와 var['table_header_box'] 를 parser.py 에서 임의로 선언했으면 해당 태그를 사용함
    # 선언하지 않았다면 부모태그(thead, tbody) 의 자식태그를 사용해 
    # var['table_data_box'] 와 var['table_header_box'] 를 만들어 사용함

    # 시스템 빌더가 입력한 header를 신뢰함. 해당 기준에 맞춰 파싱 함수에 텍스트를 전달함
    # 페이지 내에서 제공되는 header와 다를 경우 warning 을 출력하고 진행함

    # parser.py 내에서 개별적으로 파싱 메서드를 선언하지 않을 경우
    # tools.py 내에 작성된 파싱 메서드를 사용함
    process_order = [ 
    # 실행 함수를 순서대로 선언
        _search_table_header_list,
        _compare_input_header_with_table_header,
        _map_key_name_with_table_header,
        _check_valid_key,
        _add_title_index_to_var,
        _search_table_data_list,
        _parse_total_table_data
    ]
    var['table_data_list'] = ''
    for process in process_order: 
    # 파싱 결과값은 var의 key:value 쌍으로 추가되어 반환됨
        var = process(soup=soup, var=var, key_list=key_list)
        if var['table_data_list'] == 'break': return
    result = merge_var_to_dict(key_list=key_list, var=var)
    return result


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


def str_grab(input_str, start_str, end_str, index=1, from_back=False):
    """
    String에서 시작, 끝 String으로 String 추출
    ex)
    sample = '강현 이 만든 코드'
    str_grab(sample, '이 ', ' 코드') == '만든'
    :param input_str: 전체 String
    :param start_str: 추출 대상 앞 String
    :param end_str: 추출 대상 뒷 String
    :param index: 추출 대상 앞 String이 전체에서 여러 개일 경우 숫자만큼 넘기기 가능
    :param from_back: 추출 대상 앞 String이 전체에서 여러 개일 경우 뒤에서부터 추출
    :return: String
    """
    result = ''

    while index > 0:
        index = index - 1

        if not from_back:
            start_idx = input_str.find(start_str)
        else:
            start_idx = input_str.rfind(start_str)
        if start_idx == -1:
            return ''
        input_str = input_str[start_idx + len(start_str):]

        if end_str == '':
            end_idx = len(input_str)
        else:
            end_idx = input_str.find(end_str)
        if end_idx == -1:
            return ''

        if index != 0:
            continue
        input_str = input_str[:end_idx]
        result = input_str

    return result
