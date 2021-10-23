from fastapi import FastAPI
from workers.projectManager import ProjectManager
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def hello():
    return "hello"


@app.get('/scraping-start')
async def scraping():
    manager = ProjectManager()
    manager.job_init()
    return "scraping init"

class Target(BaseModel):
    channelUrl : str

@app.post('/add-new-target-channel')
def add_new_target_channel(target : Target):
    manager = ProjectManager()
    result = manager.new_target_init(target.channelUrl)
    return result
