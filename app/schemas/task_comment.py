from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCommentCreate(BaseModel):
    content: str


class TaskCommentUpdate(BaseModel):
    content: str


class UserMiniResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class TaskCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    user_id: int
    user: UserMiniResponse

    content: str

    created_at: datetime
    updated_at: datetime