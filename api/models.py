from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    completed: bool = False
    created_at: str
    updated_at: Optional[str] = None
