from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.task_comment import (
    TaskCommentCreate,
    TaskCommentUpdate,
    TaskCommentResponse,
)

from app.services.task_comment_service import (
    create_comment,
    get_task_comments,
    update_comment,
    delete_comment,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Task Comments"],
)


@router.post(
    "/{workspace_id}/tasks/{task_id}/comments",
    response_model=TaskCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_comment(
    workspace_id: int,
    task_id: int,
    comment_data: TaskCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_comment(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        comment_data=comment_data,
        current_user=current_user,
    )


@router.get(
    "/{workspace_id}/tasks/{task_id}/comments",
    response_model=list[TaskCommentResponse],
)
def get_comments(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_task_comments(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )


@router.patch(
    "/{workspace_id}/comments/{comment_id}",
    response_model=TaskCommentResponse,
)
def update_task_comment(
    workspace_id: int,
    comment_id: int,
    comment_data: TaskCommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_comment(
        db=db,
        workspace_id=workspace_id,
        comment_id=comment_id,
        comment_data=comment_data,
        current_user=current_user,
    )


@router.delete(
    "/{workspace_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_comment(
    workspace_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_comment(
        db=db,
        workspace_id=workspace_id,
        comment_id=comment_id,
        current_user=current_user,
    )
    
def test_comment_activity_after_create(
    authorized_client,
    workspace,
    task,
):
    authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/comments",
        json={
            "content": "First comment",
        },
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/logs"
    )

    assert response.status_code == 200

    logs = response.json()

    assert logs[0]["action"] == "COMMENT_CREATED"
    
def test_comment_activity_after_delete(
    authorized_client,
    workspace,
    comment,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/comments/{comment['id']}"
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/logs"
    )

    logs = response.json()

    assert logs[0]["action"] == "COMMENT_DELETED"