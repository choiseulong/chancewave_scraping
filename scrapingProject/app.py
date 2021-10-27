from fastapi import FastAPI
from workers.projectManager import ProjectManager
from pydantic import BaseModel
from datetime import datetime, timedelta
from pytz import timezone

app = FastAPI()

now = datetime.now(timezone('Asia/Seoul'))
todayString = now.strftime('%Y-%m-%d')
before2WeekString = (now-timedelta(days=7)).strftime('%Y-%m-%d')

class TargetDate(BaseModel):
    startDate : str = todayString # 오늘 부터
    endDate : str = before2WeekString # 2주 전까지

@app.post("/scraping-start-with-date")
async def scraping_with_target_date(targetDate : TargetDate):
    inputDate = targetDate.dict()
    if check_input_date_vaildation(inputDate) == 'vaild':
        manager = ProjectManager()
        manager.job_init_with_target_date(inputDate)
    else :
        return "날짜 입력 형식을 확인해 주세요"

def check_input_date_vaildation(inputDate):
    startDate = datetime.strptime(inputDate["startDate"], "%Y-%m-%d").isoformat()
    endDate = datetime.strptime(inputDate["endDate"], "%Y-%m-%d").isoformat()
    if startDate >= endDate :
        return 'vaild'
    else :
        return
