from datetime import datetime
from pytz import timezone
import string

def get_channel_data_frame(channelName, channelUrl, count):
    now = datetime.now(timezone('Asia/Seoul'))
    channelCode = make_channel_code(count)
    return {
        'channelName' : channelName,
        'channelCode' : channelCode,
        'channelUrl' : {channelCode+str(idx) : url for idx, url in enumerate(channelUrl)},
        'createdTime' : now,
        'updateTime' : '',
        'contentsUrl' : {channelCode+str(idx) : [] for idx in range(len(channelUrl))}
    }

def make_channel_code(count):
    '''
        26*26개까지 처리 가능
    '''
    if count > 676:
        raise Exception('새로운 채널을 DB에 반영할 수 없습니다.')
    channelCode = ''
    share, remainder = divmod(count, 26)
    if share :
        channelCode += string.ascii_lowercase[share-1]
    channelCode += string.ascii_lowercase[remainder]
    return channelCode

