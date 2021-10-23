from datetime import datetime
from pytz import timezone
import string

def get_channel_data_frame(channelName, channelUrl, count):
    now = datetime.now(timezone('Asia/Seoul'))
    channelCode = make_channel_code(count)
    return {
        'channelName' : channelName,
        'channelCode' : channelCode,
        'channelUrl' : [{channelCode+str(idx) : url} for idx, url in enumerate(channelUrl)],
        'createdTime' : now,
        'updateTime' : '',
        'contentsUrl' : [{channelCode+str(idx) : []} for idx in range(len(channelUrl))]
    }

def make_channel_code(count):
    channelCode = ''
    share, remainder = divmod(count, 26)
    if share:
        channelCode += string.ascii_lowercase[share-1]
    channelCode += string.ascii_lowercase[remainder]
    return channelCode

