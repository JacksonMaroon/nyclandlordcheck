"""Expand DOB violation column lengths

Revision ID: 002
Revises: 001
Create Date: 2026-01-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "dob_violations",
        "isn_dob_bis_viol",
        existing_type=sa.String(length=20),
        type_=sa.String(length=50),
    )
    op.alter_column(
        "dob_violations",
        "house_number",
        existing_type=sa.String(length=20),
        type_=sa.String(length=50),
    )
    op.alter_column(
        "dob_violations",
        "number",
        existing_type=sa.String(length=20),
        type_=sa.String(length=50),
    )


def downgrade() -> None:
    op.alter_column(
        "dob_violations",
        "number",
        existing_type=sa.String(length=50),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "dob_violations",
        "house_number",
        existing_type=sa.String(length=50),
        type_=sa.String(length=20),
    )
    op.alter_column(
        "dob_violations",
        "isn_dob_bis_viol",
        existing_type=sa.String(length=50),
        type_=sa.String(length=20),
    )
