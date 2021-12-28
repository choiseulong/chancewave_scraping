from fastapi import FastAPI
from workers.project_manager import ProjectManager
from pydantic import BaseModel
from datetime import datetime, timedelta
from pytz import timezone

app = FastAPI()

now = datetime.now(timezone('Asia/Seoul'))
todayString = now.strftime('%Y-%m-%d %H:%M:%S')
before2WeekString = (now-timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

class TargetDate(BaseModel):
    start_date : str = todayString # 오늘 부터
    end_date : str = before2WeekString # 2주 전까지

@app.post("/scraping-start")
async def scraping_with_target_date(targetDate : TargetDate):
    inputDate = targetDate.dict()
    if check_input_date_vaildation(inputDate) == 'vaild':
        manager = ProjectManager()
        manager.job_init_with_target_date(inputDate)
    else :
        return "날짜 입력 형식을 확인해 주세요"

@app.get('/scraping-test/{channel_code}')
def scraping_test(channel_code : str):
    manager = ProjectManager()
    manager.scraping_test(channel_code)


def check_input_date_vaildation(inputDate):
    start_date = inputDate["start_date"]
    end_date = inputDate["end_date"]

    if ":" not in start_date:
        start_date += " 23:59:59"

    if ":" not in end_date:
        end_date += " 00:00:01"

    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").isoformat()
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").isoformat()

    if start_date >= end_date :
        return 'vaild'
    else :
        return

@app.get('/getChannelData/')
def get_channel_data(channel_code : str = ''):
    manager = ProjectManager()
    data = manager.get_data(channel_code)
    return data

@app.get('/getTotalData')
def get_total_data():
    manager = ProjectManager()
    data = manager.get_data()
    return data
