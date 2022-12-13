from fastapi import FastAPI
from workers.project_manager import ProjectManager
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/scraping-start")
async def scraping_with_target_date():
    manager = ProjectManager()
    message = manager.job_init()
    return message

@app.get('/')
def main():
    return 'chancewave scraper'

class INITIAL_PROCESS_SOURCE(BaseModel):
    channel_code : Optional[str] = ''
    count : int

@app.post('/get-channel-data')
async def get_channel_data(SOURCE:INITIAL_PROCESS_SOURCE):
    channel_code = SOURCE.channel_code
    count = SOURCE.count
    manager = ProjectManager()
    data = manager.get_data(channel_code, count)
    return data

@app.post('/get-total-channel-data')
async def get_total_data(SOURCE :INITIAL_PROCESS_SOURCE):
    channel_code = SOURCE.channel_code
    count = SOURCE.count
    manager = ProjectManager()
    data = manager.get_data(channel_code, count)
    return data
