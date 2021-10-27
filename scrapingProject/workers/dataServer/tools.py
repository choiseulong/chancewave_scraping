import zlib
from datetime import datetime
from pytz import timezone

def make_crc(data):
    text = ''
    for key in data:
        if isinstance(data[key], str):
            text += data[key]
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

def update_data(newData, beforeData):
    now = datetime.now(timezone('Asia/Seoul')).isoformat()
    for key in beforeData :
        if key != '_id':
            beforeData[key] = newData[key]
    beforeData['isupdated'] = not beforeData['isupdated']
    beforeData['updatedTime'] = now
    return beforeData