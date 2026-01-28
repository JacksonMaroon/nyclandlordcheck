"""Expand evictions ejectment length

Revision ID: 005
Revises: 004
Create Date: 2026-01-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "evictions",
        "ejectment",
        existing_type=sa.String(length=10),
        type_=sa.String(length=50),
    )


def downgrade() -> None:
    op.alter_column(
        "evictions",
        "ejectment",
        existing_type=sa.String(length=50),
        type_=sa.String(length=10),
    )
