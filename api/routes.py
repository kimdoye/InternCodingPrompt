from fastapi import APIRouter, status
from .controllers import get_tasks, get_task, create_task, update_task, delete_task, health
from .models import Task, TaskCreate, TaskUpdate
from typing import List

router = APIRouter()

# Define routes
@router.get('/tasks', response_model=List[Task])
def read_tasks():
    return get_tasks()

@router.get('/tasks/{task_id}', response_model=Task)
def read_task(task_id: str):
    return get_task(task_id)

@router.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
def post_task(task: TaskCreate):
    return create_task(task)

@router.put('/tasks/{task_id}', response_model=Task)
def put_task(task_id: str, task: TaskUpdate):
    return update_task(task_id, task)

@router.delete('/tasks/{task_id}')
def remove_task(task_id: str):
    return delete_task(task_id)

@router.get('/health')
def get_health():
    return health()
