from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.constants.roles import WorkspaceRole

from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.services.workspace_service import get_workspace
from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
)



def get_membership(
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

    return membership

def require_membership(
    db: Session,
    workspace_id: int,
    user_id: int,
):
    membership = get_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    return membership



def create_member(
    db: Session,
    workspace_id: int,
    member_data: WorkspaceMemberCreate,
    current_user: User,
):
    get_workspace(
        db=db,
        workspace_id=workspace_id,
    )

    membership = require_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    if membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can add members",
        )

    user = (
        db.query(User)
        .filter(
            User.id == member_data.user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_member = get_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=member_data.user_id,
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member",
        )

    new_member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=member_data.user_id,
        role=member_data.role,
    )

    try:
        db.add(new_member)
        db.commit()
        db.refresh(new_member)

    except Exception:
        db.rollback()
        raise

    return new_member


def get_workspace_members(
    db: Session,
    workspace_id: int,
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

    return (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id
        )
        .all()
    )
    
def update_workspace_member_role(
    db: Session,
    workspace_id: int,
    user_id: int,
    role: WorkspaceRole,
    current_user: User,
):
    get_workspace(
        db=db,
        workspace_id=workspace_id,
    )

    membership = require_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    if membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can update member roles",
        )
    member = get_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )
    if member.role == WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner role cannot be changed",
        )

    if role == WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign owner role",
        )

    if member.role == role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Member already has this role",
        )
    member.role = role

    try:
        db.commit()
        db.refresh(member)

    except Exception:
        db.rollback()
        raise

    return member


def remove_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int,
    current_user: User,
):
    get_workspace(
    db=db,
    workspace_id=workspace_id,
)

    membership = require_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )
    if membership.role != WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can remove members",
        )
    member = get_membership(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found",
        )
    if member.role == WorkspaceRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot be removed",
        )
    if member.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot remove themselves",
        )
    try:
        db.delete(member)
        db.commit()

    except Exception:
        db.rollback()
        raise