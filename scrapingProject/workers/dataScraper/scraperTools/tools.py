from time import sleep
import json
from datetime import datetime
from pytz import timezone

def get_method_response(session, url, header={}):
    response = session.get(url, header=header)
    sleep(1)
    return response.status_code, response

def post_method_response(session, url, header={}, data={}):
    data = json.dumps(json)
    response = session.post(url, header=header, data=data)
    sleep(1)
    return response.status_code, response

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


def get_data_frame(channelCode, channelUrl):
    now = datetime.now(timezone('Asia/Seoul'))
    return {
        'channelCode' : channelCode,
        'channelUrl' : channelUrl,
        'createdTime' : now,
        'postTitle' : '',
        'postContents' : {
            'postText' : '',
            'postImageUrl': []
        },
        'viewCount' : 0,
        'uploadTime' : '',
        'uploader' : '',
        'isUpdate' : False,
        'updateTime' : '',
    }