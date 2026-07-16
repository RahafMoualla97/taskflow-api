from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
    WorkspaceMemberRoleUpdate,
    
)

from app.services.workspace_member_service import (
    create_member,
    get_workspace_members,
    update_workspace_member_role,
    remove_workspace_member,
)

router = APIRouter(
    prefix="/workspaces/{workspace_id}/members",
    tags=["Workspace Members"],
)

@router.post(
    "",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member(
    workspace_id: int,
    member_data: WorkspaceMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_member(
        db=db,
        workspace_id=workspace_id,
        member_data=member_data,
        current_user=current_user,
    )
    
    
@router.get(
    "",
    response_model=list[WorkspaceMemberResponse],
)
def list_members(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return get_workspace_members(
        db=db,
        workspace_id=workspace_id,
        current_user=current_user,
    )
    
    
@router.patch(
    "/{user_id}/role",
    response_model=WorkspaceMemberResponse,
)
def update_member_role(
    workspace_id: int,
    user_id: int,
    role_data: WorkspaceMemberRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_workspace_member_role(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
        role=role_data.role,
        current_user=current_user,
    )
    
    
@router.delete(
    "/{user_id}",
    status_code=204,
)
def remove_member(
    workspace_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    remove_workspace_member(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
        current_user=current_user,
    )