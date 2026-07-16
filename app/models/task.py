from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Task(Base):

    __tablename__ = "tasks"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    description = Column(
        Text,
        nullable=True
    )


    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )


    created_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    assigned_to_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )


    status = Column(
        String,
        nullable=False,
        default="todo"
    )


    priority = Column(
        String,
        nullable=False,
        default="medium"
    )


    due_date = Column(
        DateTime(timezone=True),
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


    workspace = relationship(
        "Workspace",
        back_populates="tasks",
    )


    comments = relationship(
        "TaskComment",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    
    creator = relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_tasks",
    )

    assignee = relationship(
        "User",
        foreign_keys=[assigned_to_id],
        back_populates="assigned_tasks",
    )
    
    logs = relationship(
        "TaskLog",
        back_populates="task",
    )