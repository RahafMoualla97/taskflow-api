from app.services.workspace_member_service import require_membership
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.task import Task
from app.models.task_log import TaskLog
from app.constants.roles import WorkspaceRole
from app.models.workspace_member import WorkspaceMember
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_log_service import create_task_log, get_task_logs
from app.services.workspace_service import get_workspace
from app.constants.task_logs import (
    TASK_CREATED,
    TASK_UPDATED,
    STATUS_CHANGED,
    PRIORITY_CHANGED,
    TITLE_CHANGED,
    DESCRIPTION_CHANGED,
    ASSIGNED_CHANGED,
    DUE_DATE_CHANGED,
    TASK_DELETED,
    TASK_RESTORED,
)

def create_task(
    db: Session,
    workspace_id: int,
    task_data: TaskCreate,
    current_user: User,
):
    get_workspace(
        db=db,
        workspace_id=workspace_id,
    )

    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )
    if task_data.assigned_to_id is not None:
        assigned_member = (
            db.query(WorkspaceMember)
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == task_data.assigned_to_id,
            )
            .first()
        )

        if assigned_member is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user is not a workspace member",
            )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        workspace_id=workspace_id,
        created_by_id=current_user.id,
        assigned_to_id=task_data.assigned_to_id,
        priority=task_data.priority,
        due_date=task_data.due_date,
    )

    try:
        db.add(new_task)
        db.flush()

        create_task_log(
            db=db,
            task_id=new_task.id,
            user_id=current_user.id,
            action=TASK_CREATED,
            message="Task created",
        )

        db.commit()
        db.refresh(new_task)

    except Exception:
        db.rollback()
        raise

    return new_task


def get_workspace_tasks(
    db: Session,
    workspace_id: int,
    current_user: User,
    page: int,
    limit: int,
    task_status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    query = (
        db.query(Task)
        .filter(
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
    )

    if task_status:
        query = query.filter(
            Task.status == task_status
        )

    if priority:
        query = query.filter(
            Task.priority == priority
        )

    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    total = query.count()

    offset = (page - 1) * limit

    tasks = (
        query
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    pages = (total + limit - 1) // limit

    return {
        "items": tasks,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
    }
    
def get_task(
    db: Session,
    workspace_id: int,
    task_id: int,
    current_user: User,
):
    get_workspace(
        db=db,
        workspace_id=workspace_id,
    )
    require_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task

def get_task_details(
    db: Session,
    workspace_id: int,
    task_id: int,
    current_user: User,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    logs = (
        db.query(TaskLog)
        .filter(
            TaskLog.task_id == task_id
        )
        .order_by(
            TaskLog.created_at.desc()
        )
        .all()
    )

    return {
        "task": task,
        "activity": logs,
    }
    
    



def get_task_activity(
    db: Session,
    workspace_id: int,
    task_id: int,
    current_user: User,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.workspace_id == workspace_id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return get_task_logs(
        db=db,
        task_id=task.id,
    )
    
def update_task(
    db: Session,
    workspace_id: int,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = task_data.model_dump(exclude_unset=True)

    if "assigned_to_id" in update_data:
        assigned_to_id = update_data["assigned_to_id"]

        if assigned_to_id is not None:
            assigned_member = (
                db.query(WorkspaceMember)
                .filter(
                    WorkspaceMember.workspace_id == workspace_id,
                    WorkspaceMember.user_id == assigned_to_id,
                )
                .first()
            )

            if assigned_member is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assigned user is not a workspace member",
                )

    old_values = {}

    for field, value in update_data.items():
        old_values[field] = getattr(task, field)

    try:
        for field, value in update_data.items():
            setattr(task, field, value)

        action_map = {
            "status": STATUS_CHANGED,
            "priority": PRIORITY_CHANGED,
            "title": TITLE_CHANGED,
            "description": DESCRIPTION_CHANGED,
            "assigned_to_id": ASSIGNED_CHANGED,
            "due_date": DUE_DATE_CHANGED,
        }

        for field, old_value in old_values.items():
            new_value = getattr(task, field)

            if old_value != new_value:
                create_task_log(
                    db=db,
                    task_id=task.id,
                    user_id=current_user.id,
                    action=action_map.get(field, TASK_UPDATED),
                    old_value=str(old_value) if old_value is not None else None,
                    new_value=str(new_value) if new_value is not None else None,
                    message=f"{field} changed",
                )

        db.commit()
        db.refresh(task)

    except Exception:
        db.rollback()
        raise

    return task

    

def delete_task(
    db: Session,
    workspace_id: int,
    task_id: int,
    current_user: User,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )
    if membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can delete tasks",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.workspace_id == workspace_id,
            Task.deleted_at.is_(None),
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    try:
        task.deleted_at = datetime.now(timezone.utc)

        create_task_log(
            db=db,
            task_id=task.id,
            user_id=current_user.id,
            action=TASK_DELETED,
            message="Task deleted",
        )

        db.commit()

    except Exception:
        db.rollback()
        raise
    
    
def restore_task(
    db: Session,
    workspace_id: int,
    task_id: int,
    current_user: User,
):
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )
    if membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can restore tasks",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.workspace_id == workspace_id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.deleted_at is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is not deleted",
        )

    try:
        task.deleted_at = None

        create_task_log(
            db=db,
            task_id=task.id,
            user_id=current_user.id,
            action=TASK_RESTORED,
            message="Task restored",
        )

        db.commit()
        db.refresh(task)

    except Exception:
        db.rollback()
        raise

    return task