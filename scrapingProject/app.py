from fastapi import FastAPI
from workers.projectManager import ProjectManager
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from pytz import timezone

app = FastAPI()

@app.get('/')
def main():
    return 'hi'

@app.get('/scraping-start')
async def scraping():
    manager = ProjectManager()
    manager.job_init()
    return "scraping init"

now = datetime.now(timezone('Asia/Seoul'))
todayString = now.strftime('%Y-%m-%d')
after2WeekString = (now+timedelta(days=14)).strftime('%Y-%m-%d')


class TargetDate(BaseModel):
    startDate : str = after2WeekString # 오늘 14일 이전이 디폴트
    endDate : str = todayString # 오늘이 디폴트


@app.post("/scraping-start-with-date")
async def scraping_with_target_date(targetDate : TargetDate):
    manager = ProjectManager()
    manager.job_init_with_target_date(targetDate.dict())



class Target(BaseModel):
    channelName : Optional[str]
    channelUrl : List[str]

@app.post('/add-new-target-channel')
def add_new_target_channel(target : Target):
    manager = ProjectManager()
    result = manager.new_target_init(target)
    return result