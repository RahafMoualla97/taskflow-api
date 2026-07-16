from app.services.task_service import get_task
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_comment import TaskComment
from app.models.workspace_member import WorkspaceMember
from app.models.user import User

from app.schemas.task_comment import (
    TaskCommentCreate,
    TaskCommentUpdate,
)
from app.services.task_log_service import create_task_log

from app.constants.task_logs import (
    COMMENT_CREATED,
    COMMENT_UPDATED,
    COMMENT_DELETED,
)
from app.services.workspace_service import get_workspace




def check_workspace_membership(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )


def create_comment(
    db: Session,
    workspace_id: int,
    task_id: int,
    comment_data: TaskCommentCreate,
    current_user: User,
):
    get_workspace(
        db=db,
        workspace_id=workspace_id,
    )

    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    get_task(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )

    comment = TaskComment(
        task_id=task_id,
        user_id=current_user.id,
        content=comment_data.content,
    )

    try:
        db.add(comment)
        db.flush()

        create_task_log(
            db=db,
            task_id=task_id,
            user_id=current_user.id,
            action=COMMENT_CREATED,
            new_value=comment.content,
            message="Comment created",
        )

        db.commit()
        db.refresh(comment)

    except Exception:
        db.rollback()
        raise

    return comment

def get_task_comments(
    db: Session,
    workspace_id: int,
    task_id: int,
    current_user: User,
):


    get_task(
        db=db,
        workspace_id=workspace_id,
        task_id=task_id,
        current_user=current_user,
    )

    return (
        db.query(TaskComment)
        .filter(
            TaskComment.task_id == task_id,
        )
        .order_by(
            TaskComment.created_at.desc()
        )
        .all()
    )


def update_comment(
    db: Session,
    workspace_id: int,
    comment_id: int,
    comment_data: TaskCommentUpdate,
    current_user: User,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    comment = (
        db.query(TaskComment)
        .join(Task)
        .filter(
            TaskComment.id == comment_id,
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments",
        )

    old_content = comment.content

    try:
        comment.content = comment_data.content

        create_task_log(
            db=db,
            task_id=comment.task_id,
            user_id=current_user.id,
            action=COMMENT_UPDATED,
            old_value=old_content,
            new_value=comment.content,
            message="Comment updated",
        )

        db.commit()
        db.refresh(comment)

    except Exception:
        db.rollback()
        raise

    return comment


def delete_comment(
    db: Session,
    workspace_id: int,
    comment_id: int,
    current_user: User,
):
    check_workspace_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    comment = (
        db.query(TaskComment)
        .join(Task)
        .filter(
            TaskComment.id == comment_id,
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments",
        )

    try:
        create_task_log(
            db=db,
            task_id=comment.task_id,
            user_id=current_user.id,
            action=COMMENT_DELETED,
            old_value=comment.content,
            message="Comment deleted",
        )

        db.delete(comment)

        db.commit()

    except Exception:
        db.rollback()
        raise
    
    
