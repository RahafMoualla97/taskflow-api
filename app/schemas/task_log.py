from datetime import datetime
from pydantic import BaseModel, ConfigDict



class UserMiniResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class TaskLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    user_id: int
    user: UserMiniResponse

    action: str
    old_value: str | None
    new_value: str | None
    message: str | None
    created_at: datetime
    