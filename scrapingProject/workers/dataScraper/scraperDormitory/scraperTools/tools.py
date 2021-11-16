from time import sleep
import json
from datetime import datetime
import datetime as DateTime
from pytz import timezone
from ..parserTools.newtools import *

def set_headers(session, additionalKeyValue=None, isUpdate=False):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    if additionalKeyValue and isUpdate:
        for keyValue in additionalKeyValue:
            headers.update({keyValue[0]:keyValue[1]})
    session.headers = headers
    return session

def get_method_response(session, url):
    response = session.get(url)
    status = 'fail'
    if response.status_code == 200 :
        status = 'ok'
    sleep(2)
    return status, response

def post_method_response(session, url, data={}, jsonize=False):
    if jsonize and data:
        data = json.dumps(data)
    response = session.post(url, data=data)
    status = 'fail'
    if response.status_code == 200 :
        status = 'ok'
    sleep(2)
    return status, response

def filtering_channel_path_in_globals(Globals):
    channelCodeList = []
    for globalVarKey in Globals.keys():
        if 'url_' in globalVarKey:
            key = globalVarKey.replace("url_", "")
            channelCodeList.append({key : Globals[f'{globalVarKey}']})
    return channelCodeList

def return_key_value(data):
    key = list(data.keys())[0]
    value = data[key]
    return key, value

def get_post_data_frame(channelCode='', channelUrl=''):
    now = datetime.now(timezone('Asia/Seoul'))
    return {
        'channelCode' : channelCode,
        'channelUrl' : channelUrl,
        'postUrl' : None,
        'linkedPostUrl': None,
        'createdTime' : now.isoformat(),
        'postTitle' : None,
        'postSubject' : None,
        'postText' : None,
        'postContentTarget' : None,
        'postTextType' : 'onlyPostText',
        'contact': None,
        'postImageUrl': None,
        'viewCount' : None,
        'uploadedTime' : None,
        'uploader' : None,
        'startDate' : None,
        'endDate' : None,
        'startDate2' : None,
        'endDate2' : None,
        'isUpdate' : False,
        'updatedTime' : None,
        'crc' : None,
        'extraInfo' : []
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
        if key in dataFrame.keys():
            dataFrame[key] = result[key]
    return dataFrame

def find_request_params(data, paramsKey):
    params = []
    for key in paramsKey:
        P = [k for k in data if key in k.keys()]
        if P:
            params.append((key,P[0][key]))
    return params
