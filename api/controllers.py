import uuid
from datetime import datetime, UTC
from fastapi import HTTPException
from .models import Task, TaskCreate, TaskUpdate

# In-memory storage for tasks
tasks = {}


def get_tasks():
    """Read: Get all tasks"""
    return list(tasks.values())


def get_task(task_id: str):
    """Read: Get a specific task by ID"""
    task = tasks.get(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail={"error": "Task not found"})


def create_task(task_in: TaskCreate):
    """Create: Create a new task"""
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": task_in.title,
        "description": task_in.description or "",
        "completed": False,
        "created_at": datetime.now(UTC).isoformat(),
    }

    tasks[task_id] = task
    return task


def update_task(task_id: str, task_in: TaskUpdate):
    """Update: Update an existing task"""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    # Update task fields
    if task_in.title is not None:
        task["title"] = task_in.title
    if task_in.description is not None:
        task["description"] = task_in.description
    if task_in.completed is not None:
        task["completed"] = task_in.completed

    task["updated_at"] = datetime.now(UTC).isoformat()
    tasks[task_id] = task

    return task


def delete_task(task_id: str):
    """Delete: Delete a task"""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})

    del tasks[task_id]
    return {"message": "Task deleted successfully"}


def health():
    """Health check endpoint"""
    return {"status": "healthy"}
