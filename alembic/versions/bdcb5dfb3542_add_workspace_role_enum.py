"""add workspace role enum

Revision ID: bdcb5dfb3542
Revises: 99b146080d11
Create Date: 2026-07-11 00:16:22.055787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdcb5dfb3542'
down_revision: Union[str, Sequence[str], None] = '99b146080d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    workspacerole = sa.Enum(
        'OWNER',
        'ADMIN',
        'MEMBER',
        name='workspacerole'
    )

    workspacerole.create(op.get_bind())

    op.alter_column(
        'workspace_members',
        'role',
        existing_type=sa.VARCHAR(),
        type_=workspacerole,
        existing_nullable=False,
        postgresql_using="role::workspacerole",
    )


def downgrade() -> None:
    workspacerole = sa.Enum(
        'OWNER',
        'ADMIN',
        'MEMBER',
        name='workspacerole'
    )

    op.alter_column(
        'workspace_members',
        'role',
        existing_type=workspacerole,
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    workspacerole.drop(op.get_bind())