from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.constants.roles import WorkspaceRole


class WorkspaceMemberCreate(BaseModel):
    user_id: int
    role: WorkspaceRole = WorkspaceRole.MEMBER



class MemberUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class WorkspaceMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    workspace_id: int
    role: WorkspaceRole

    user: MemberUserResponse

    created_at: datetime
    
class WorkspaceMemberRoleUpdate(BaseModel):
    role: WorkspaceRole