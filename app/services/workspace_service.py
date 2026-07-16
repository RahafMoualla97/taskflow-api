from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.constants.roles import WorkspaceRole
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate
from app.services.user_service import get_user_by_id

def create_workspace(
    db: Session,
    workspace_data: WorkspaceCreate,
    current_user: User
):
    new_workspace = Workspace(
        name=workspace_data.name,
        owner_id=current_user.id
    )

    try:
        db.add(new_workspace)
        db.flush()

        workspace_member = WorkspaceMember(
            workspace_id=new_workspace.id,
            user_id=current_user.id,
            role=WorkspaceRole.OWNER
        )

        db.add(workspace_member)

        db.commit()
        db.refresh(new_workspace)

    except Exception:
        db.rollback()
        raise

    return new_workspace

def get_workspace(
    db: Session,
    workspace_id: int,
):
    workspace = (
        db.query(Workspace)
        .filter(
            Workspace.id == workspace_id,
        )
        .first()
    )

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return workspace

def get_my_workspaces(db: Session, current_user: User):
    return (
        db.query(Workspace)
        .join(
            WorkspaceMember,
            WorkspaceMember.workspace_id == Workspace.id
        )
        .filter(
            WorkspaceMember.user_id == current_user.id
        )
        .all()
    )



