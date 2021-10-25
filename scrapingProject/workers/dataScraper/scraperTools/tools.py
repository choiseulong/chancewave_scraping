from time import sleep
import json
from datetime import datetime
import datetime as DateTime
from pytz import timezone

def get_method_response(session, url, header={}):
    response = session.get(url, headers=header)
    status = 'fail'
    if response.status_code == 200 :
        status = 'ok'
    sleep(1)
    return status, response

def post_method_response(session, url, header={}, data={}):
    data = json.dumps(data)
    response = session.post(url, headers=header, data=data)
    status = 'fail'
    if response.status_code == 200 :
        status = 'ok'
    sleep(1)
    return status, response

def filtering_channel_path_in_globals(Globals):
    channelCodeList = []
    for globalVarKey in Globals.keys():
        if 'url_' in globalVarKey:
            key = globalVarKey.replace("url_", "")
            channelCodeList.append({key : Globals[f'{globalVarKey}']})
    return channelCodeList

def search_channel_path_in_globals(Globals, channelCode):
    channelUrl = {channelCode : Globals[f'url_{channelCode}']}
    return channelUrl

def return_key_value(data):
    key = list(data.keys())[0]
    value = data[key]
    return key, value

def get_post_data_frame(channelCode='', channelUrl=''):
    now = datetime.now(timezone('Asia/Seoul'))
    return {
        'channelCode' : channelCode,
        'channelUrl' : channelUrl,
        'contentsUrl' : '',
        'createdTime' : now,
        'postTitle' : '',
        'postContents' : {
            'postSubject' : '',
            'postText' : '',
            'contact': '',
            'postImageUrl': []
        },
        'viewCount' : 0,
        'uploadTime' : '',
        'uploader' : '',
        'isUpdate' : False,
        'updateTime' : '',
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

def enter_data_into_dataFrame(dataFrame, result):
    for key in result:
        keyRoot = find_key_root(key)
        if not keyRoot:
            if isinstance(result[key], DateTime.date):
                dataFrame[key] = result[key]
                continue
            dataFrame[key] += result[key]
        else :
            dataFrame[keyRoot][key] += result[key]
    return dataFrame


def get_channel_data_frame(channelCode, channelUrl):
    now = datetime.now(timezone('Asia/Seoul'))
    return {
        'channelCode' : channelCode,
        'channelUrl' : channelUrl,
        'createdTime' : now,
        'updateTime' : '',
        'contentsUrl' : []
    }
