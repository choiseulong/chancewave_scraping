from time import sleep
import json
from datetime import datetime
from pytz import timezone
from ..parser_tools.tools import *
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def set_headers(session, additional_key_value=None, is_update=False):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    if additional_key_value and is_update:
        for key_value in additional_key_value:
            headers.update({key_value[0]: key_value[1]})
    session.headers = headers
    return session


def extract_channel_board_num(channel_code):
    """
    채널 코드에서 채널의 게시판 번호를 추출
    :param channel_code: 채널 코드
    :return: int - 게시판 번호

    example)
    input string "jeonnam__jeonnamdo_0"
    output int   0
    """
    if channel_code.find('_') < 0:
        return None
    else:
        channel_board_num = channel_code.split('_')[-1]
        return int(channel_board_num)


def get_method_response(session, url, sleep_sec=2):
    response = session.get(url, verify=False)
    status = 'fail'
    if response.status_code == 200:
        status = 'ok'
    sleep(sleep_sec)
    return status, response

def post_method_response(session, url, data={}, sleep_sec=2, jsonize=False):
    if jsonize :
        data = json.dumps(data)
    response = session.post(url, data=data, verify=False)
    status = 'fail'
    if response.status_code == 200:
        status = 'ok'
    sleep(sleep_sec)
    return status, response

def filtering_channel_path_in_globals(globals):
    channel_code_list = []
    for global_var_key in globals.keys():
        if 'url_' in global_var_key:
            key = global_var_key.replace("url_", "")
            channel_code_list.append({key : globals[f'{global_var_key}']})
    return channel_code_list


def return_key_value(data):
    key = list(data.keys())[0]
    value = data[key]
    return key, value


def get_post_data_frame(
        channel_code='',
        channel_url='',
        post_url_can_use=True,
        channel_name='',
        post_board_name=''
    ):
    now = datetime.now(timezone('Asia/Seoul'))
    return {
        'channel_name' : channel_name,
        'post_board_name' : post_board_name,
        'channel_code' : channel_code,
        'channel_url' : channel_url,
        'post_url' : None,
        'post_url_can_use' : post_url_can_use,
        'linked_post_url': None,
        'created_time' : now.isoformat(),
        'post_title' : None,
        'post_subject' : None,
        'post_text' : None,
        'post_content_target' : None,
        'post_text_type' : 'only_post_text',
        'contact': None,
        'post_image_url': None,
        'post_thumbnail' : '',
        'view_count' : None,
        'uploaded_time' : None,
        'uploader' : None,
        'start_date' : None,
        'end_date' : None,
        'start_date2' : None,
        'end_date2' : None,
        'is_update_check_time' : [],
        'updated_time' : [],
        'is_going_on' : None,
        'crc' : None,
        'extra_info' : []
    }


def find_key_root(key_name) :
    frame = get_post_data_frame()
    value = frame.get(key_name)
    if value is not None:
        return
    else :
        for key in frame.keys():
            if type(frame[key]) == dict:
                value = frame[key].get(key_name)
                if value is not None:
                    return key


def enter_data_into_dataFrame(dataFrame, result):
    for key in result:
        if key in dataFrame.keys():
            dataFrame[key] = result[key]
    return dataFrame


def find_request_params(data, params_key):
    params = []
    for key in params_key:
        tmp_param = [k for k in data if key in k.keys()]
        if tmp_param:
            params.append((key, tmp_param[0][key]))
    return params
