from datetime import datetime
from typing import Optional
from app.schemas.task_log import TaskLogResponse
from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar

T = TypeVar("T")


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None

    workspace_id: int

    created_by_id: int
    assigned_to_id: Optional[int]

    status: str
    priority: str

    due_date: Optional[datetime]

    created_at: datetime
    updated_at: datetime
    
    
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    pages: int
    
    
class TaskDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task: TaskResponse
    activity: list[TaskLogResponse]