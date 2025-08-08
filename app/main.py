from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult

# Import the celery task
from app.celery_worker import create_video_task

app = FastAPI()

class ProjectCreate(BaseModel):
    title: str
    script: str

@app.post("/api/create_project")
def create_project(project: ProjectCreate):
    """Endpoint to create a new video generation task."""
    # Send the task to the Celery queue
    task = create_video_task.delay(project.script)
    return {"task_id": task.id}

@app.get("/api/project/{task_id}/status")
def get_task_status(task_id: str):
    """Endpoint to check the status of a task."""
    task_result = AsyncResult(task_id, app=create_video_task.app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result or None
    }
    
    if task_result.status == 'PROGRESS':
        response['result'] = task_result.info
    elif task_result.status == 'FAILURE':
        response['result'] = {'message': str(task_result.info)}
        
    return response
