from sqlalchemy.orm import Session

from app.models.task_log import TaskLog

def create_task_log(
    db: Session,
    task_id: int,
    user_id: int,
    action: str,
    old_value: str | None = None,
    new_value: str | None = None,
    message: str | None = None,
    ):
    new_log = TaskLog(
    task_id=task_id,
    user_id=user_id,
    action=action,
    old_value=old_value,
    new_value=new_value,
    message=message,
    )

    db.add(new_log)

    return new_log

def get_task_logs(
    db: Session,
    task_id: int,
):
    return (
        db.query(TaskLog)
        .filter(
            TaskLog.task_id == task_id
        )
        .order_by(
            TaskLog.created_at.desc()
        )
        .all()
    )