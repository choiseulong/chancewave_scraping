from fastapi import FastAPI
from workers.projectManager import ProjectManager
from pydantic import BaseModel
from datetime import datetime, timedelta
from pytz import timezone

app = FastAPI()

now = datetime.now(timezone('Asia/Seoul'))
todayString = now.strftime('%Y-%m-%d %H:%M:%S')
before2WeekString = (now-timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

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
    startDate = inputDate["startDate"]
    endDate = inputDate["endDate"]

    if ":" not in startDate:
        startDate += " 23:59:59"

    if ":" not in endDate:
        endDate += " 00:00:01"

    endDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S").isoformat()
    startDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S").isoformat()

    if startDate >= endDate :
        return 'vaild'
    else :
        return

def start_scraping(startDate, endDate):
    print(startDate, endDate)
    
if __name__ == '__main__':
    print("날짜 입력 형식 : 2021-11-01 혹은 21-11-01\n미입력 시 최근 2주로 설정")
    startDate = input("시작 일자 :").strip()
    endDate = input("마지막 일자 :").strip()
    if not startDate or not endDate:
        startDate = '2021-11-01'
        endDate = '2021-10-15'
    start_scraping(startDate, endDate)
