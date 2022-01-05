from fastapi import FastAPI
from workers.project_manager import ProjectManager
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# from pytz import timezone

app = FastAPI()

#now = datetime.now(timezone('Asia/Seoul'))
#todayString = now.strftime('%Y-%m-%d %H:%M:%S')
#before2WeekString = (now-timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

#class TargetDate(BaseModel):
#    start_date : str = todayString # 오늘 부터
#    end_date : str = before2WeekString # 2주 전까지

@app.get("/scraping-start")
async def scraping_with_target_date():
    manager = ProjectManager()
    manager.job_init()

# def check_input_date_vaildation(inputDate):
#     start_date = inputDate["start_date"]
#     end_date = inputDate["end_date"]

#     if ":" not in start_date:
#         start_date += " 23:59:59"

#     if ":" not in end_date:
#         end_date += " 00:00:01"

#     end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").isoformat()
#     start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").isoformat()

#     if start_date >= end_date :
#         return 'vaild'
#     else :
#         return

@app.get('/dev-test/')
def test(channel_code:str=''):
    manager = ProjectManager()
    manager.scraping_dev_test(channel_code)

@app.get('/getChannelData/')
def get_channel_data(channel_code:str=''):
    manager = ProjectManager()
    data = manager.get_data(channel_code)
    return data

@app.get('/getTotalData')
def get_total_data():
    manager = ProjectManager()
    data = manager.get_data()
    return data
