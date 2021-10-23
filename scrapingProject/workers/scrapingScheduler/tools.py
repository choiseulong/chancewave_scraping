from datetime import datetime
from pytz import timezone

def get_data_frame(channelUrl):
    now = datetime.now(timezone('Asia/Seoul'))
    return {
        'channelCode' : '',
        'channelUrl' : channelUrl,
        'createdTime' : now,
        'updateTime' : '',
        'contentsUrl' : []
    }