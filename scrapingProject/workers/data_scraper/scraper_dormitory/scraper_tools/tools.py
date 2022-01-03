from time import sleep
import json
from datetime import datetime
from pytz import timezone
from ..parser_tools.tools import *
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.HeaderParsingError)

def set_headers(session, additional_key_value=None, isUpdate=False):
    headers = {
        "Connection": "keep-alive",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    if additional_key_value and isUpdate:
        for key_value in additional_key_value:
            headers.update({key_value[0]:key_value[1]})
    session.headers = headers
    return session

def get_method_response(session, url, sleep_sec=2):
    # response = session.get(url)
    response = session.get(url, verify=False)

    status = 'fail'
    if response.status_code == 200 :
        status = 'ok'
    sleep(sleep_sec)
    return status, response

def post_method_response(session, url, data={}, sleep_sec=2, jsonize=False):
    if jsonize :
        data = json.dumps(data)
    response = session.post(url, data=data, verify=False)
    status = 'fail'
    if response.status_code == 200 :
        status = 'ok'
    sleep(sleep_sec)
    return status, response

def filtering_channel_path_in_globals(Globals):
    channel_code_list = []
    for global_var_key in Globals.keys():
        if 'url_' in global_var_key:
            key = global_var_key.replace("url_", "")
            channel_code_list.append({key : Globals[f'{global_var_key}']})
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

def find_key_root(keyName) : 
    frame = get_post_data_frame()
    value = frame.get(keyName)
    if value is not None:
        return 
    else :
        for key in frame.keys():
            if type(frame[key]) == dict :
                value = frame[key].get(keyName)
                if value is not None :
                    return key

def enter_data_into_data_frame(data_frame, result):
    for key in result:
        if key in data_frame.keys():
            data_frame[key] = result[key]
    return data_frame

def find_request_params(data, paramsKey):
    params = []
    for key in paramsKey:
        P = [k for k in data if key in k.keys()]
        if P:
            params.append((key,P[0][key]))
    return params
