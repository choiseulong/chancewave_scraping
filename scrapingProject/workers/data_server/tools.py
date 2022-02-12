import zlib
import json
from datetime import datetime

def make_crc(data):
    text = ''
    key_list = ['channel_code', 'post_title', 'post_text', 'post_subject', 'contact', 'extra_info', 'is_going_on', 'post_image_url', 'view_count']
    for key in key_list:
        if isinstance(data[key], str):
            text += data[key]
        elif isinstance(data[key], int):
            text += str(data[key])
        elif isinstance(data[key], list):
            for info_element in data[key]:
                if isinstance(info_element, dict):
                    info_element = json.dumps(info_element)
                text += ', '.join(info_element)
        else :
            continue
    if text :
        binary_text = convert_text_to_binary(text)
        crc32 = zlib.crc32(binary_text)
        return crc32

def convert_text_to_binary(input_string):
    text = (''.join(format(ord(x), 'b') for x in input_string))
    binary_text = text.encode('ascii') 
    return binary_text

def convert_datetime_to_isoformat(post_date):
    if isinstance(post_date, datetime):
        return post_date.isoformat()
    else :
        raise Exception('convert_datetime_to_isoformat, post_date 타입 에러')