from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.dependencies import get_db
from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    PaginatedResponse,
    TaskDetailsResponse,
)

from app.schemas.task_log import TaskLogResponse

from app.services.task_service import (
    create_task,
    get_workspace_tasks,
    get_task,
    update_task,
    get_task_activity,
    get_task_details,
    delete_task,
    restore_task,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Tasks"],
)

@router.post(
    "/{workspace_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_in_workspace(
    workspace_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(
        db=db,
        workspace_id=workspace_id,
        task_data=task_data,
        current_user=current_user,
    )


@router.get(
    "/{workspace_id}/tasks",
    response_model=PaginatedResponse[TaskResponse],
)
def get_tasks_in_workspace(
    workspace_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    task_status: str | None = Query(None),
    priority: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_workspace_tasks(
        db=db,
        workspace_id=workspace_id,
        current_user=current_user,
        page=page,
        limit=limit,
        task_status=task_status,
        priority=priority,
        search=search,
    )
    

    
@router.get(
    "/{workspace_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
def get_workspace_task(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_task(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )
    
@router.patch(
    "/{workspace_id}/tasks/{task_id}",
    response_model=TaskResponse,
    )
def update_workspace_task(
    workspace_id: int,
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    return update_task(
    db=db,
    workspace_id=workspace_id,
    task_id=task_id,
    task_data=task_data,
    current_user=current_user,
    )
    
    
@router.delete(
    "/{workspace_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace_task(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_task(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )
    

@router.patch(
    "/{workspace_id}/tasks/{task_id}/restore",
    response_model=TaskResponse,
)
def restore_workspace_task(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return restore_task(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )
    
    
    
@router.get(
    "/{workspace_id}/tasks/{task_id}/logs",
    response_model=list[TaskLogResponse]
)
def get_task_logs_endpoint(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_task_activity(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )



@router.get(
    "/{workspace_id}/tasks/{task_id}/details",
    response_model=TaskDetailsResponse,
)
def get_task_details_endpoint(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_task_details(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )
    

