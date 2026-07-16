from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Enum,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.constants.roles import WorkspaceRole

class WorkspaceMember(Base):

    __tablename__ = "workspace_members"


    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "user_id",
            name="uq_workspace_member"
        ),
    )


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    role = Column(
        Enum(WorkspaceRole),
        nullable=False,
        default=WorkspaceRole.MEMBER,
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    workspace = relationship(
        "Workspace",
        back_populates="members",
    )


    user = relationship(
        "User",
        back_populates="workspace_memberships",
    )