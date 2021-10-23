from fastapi import FastAPI
from workers.projectManager import ProjectManager
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

@app.get('/')
def main():
    return 'hi'

@app.get('/scraping-start')
async def scraping():
    manager = ProjectManager()
    manager.job_init()
    return "scraping init"

class Target(BaseModel):
    channelName : Optional[str]
    channelUrl : List[str]

@app.post('/add-new-target-channel')
def add_new_target_channel(target : Target):
    manager = ProjectManager()
    result = manager.new_target_init(target)
    return result