from fastapi import FastAPI, BackgroundTasks
from workers.project_manager import ProjectManager
from pydantic import BaseModel
from typing import Optional
from time import sleep

app = FastAPI()

# update target channel scraping
# @app.get("/scraping-start")
# async def scraping_with_target_date(Background_tasks : BackgroundTasks):
#     def run():
#         while True:
#             manager = ProjectManager()
#             message = manager.job_init(target=True)
#             sleep(7200) # 2 hours
#     Background_tasks.add_task(run)

# lagacy total channel scraping
@app.get("/scraping-start")
async def scraping_with_target_date(Background_tasks : BackgroundTasks):
    def run():
        while True:
            manager = ProjectManager()
            message = manager.job_init()
            sleep(43200) # 12 hours
    Background_tasks.add_task(run)

@app.get('/')
def main():
    return 'chancewave scraper'

class INITIAL_PROCESS_SOURCE(BaseModel):
    channel_code : Optional[str] = ''
    pagesize : int = 10
    page : int = 0

@app.post('/get-channel-data')
async def get_channel_data(SOURCE:INITIAL_PROCESS_SOURCE):
    channel_code = SOURCE.channel_code
    count = SOURCE.pagesize
    page = SOURCE.page
    manager = ProjectManager()
    data = manager.get_data(channel_code, count, page)
    return data

# @app.post('/get-total-channel-data')
# async def get_total_data(SOURCE :INITIAL_PROCESS_SOURCE):
#     channel_code = SOURCE.channel_code
#     count = SOURCE.count
#     manager = ProjectManager()
#     data = manager.get_data(channel_code, count)
#     return data

class DEV_SOURCE(BaseModel):
    channel_code : str

from datetime import datetime

@app.post('/dev-test')
async def test(DEV_SOURCE :DEV_SOURCE):
    now = datetime.now()
    channel_code = DEV_SOURCE.channel_code
    manager = ProjectManager()
    manager.scraping_dev_test(channel_code)
    print(datetime.now() - now)