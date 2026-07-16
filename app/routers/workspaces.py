from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import Query
from app.auth.dependencies import get_current_user
from app.dependencies import get_db
from app.models.user import User
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,

    )
from app.services.workspace_service import (
    create_workspace,
    get_my_workspaces,

    )
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    PaginatedResponse,
    TaskDetailsResponse,
)
from app.services.task_service import (
    create_task,
    get_workspace_tasks,
    update_task,
    get_task_activity,
    get_task_details,
    delete_task,
    restore_task,
    get_task,
    )
from app.schemas.task_log import TaskLogResponse
from typing import Optional

router = APIRouter(
prefix="/workspaces",
tags=["Workspaces"],
)

@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
    )
def create_new_workspace(
    workspace_data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    return create_workspace(
    db=db,
    workspace_data=workspace_data,
    current_user=current_user,
    )

@router.get("", response_model=list[WorkspaceResponse])
def get_my_workspaces_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    return get_my_workspaces(
    db=db,
    current_user=current_user,
    )





