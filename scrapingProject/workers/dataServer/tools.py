import zlib
from datetime import datetime
from pytz import timezone

def make_crc(data):
    text = ''
    keyList = ['channelCode', 'channelUrl', 'postUrl', 'postTitle', 'postText', 'postSubject', 'contact', 'extraInfo', 'isGoingOn']
    for key in keyList:
        if isinstance(data[key], str):
            text += data[key]
        elif isinstance(data[key], list):
            for infoElement in data[key]:
                text += ', '.join(infoElement)
        else :
            continue
    if text :
        binaryText = convert_text_to_binary(text)
        crc32 = zlib.crc32(binaryText)
        return crc32

def convert_text_to_binary(input_string):
    text = (''.join(format(ord(x), 'b') for x in input_string))
    binaryText = text.encode('ascii') 
    return binaryText

def convert_datetime_to_isoformat(postDate):
    if isinstance(postDate, datetime):
        return postDate.isoformat()
    else :
        raise Exception('convert_datetime_to_isoformat, postDate 타입 에러')