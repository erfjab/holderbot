"""Refactor settings table

Revision ID: 4abf3adb8ab8
Revises: ab1ce3ef2a57
Create Date: 2024-11-08 02:42:49.391685

"""
# pylint: disable=all

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = "4abf3adb8ab8"
down_revision: Union[str, None] = "ab1ce3ef2a57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Refactor settings table by dropping the old table and creating a new structure."""
    # Drop the old settings table
    op.drop_table("settings")  # pylint: disable=no-member

    # Recreate the settings table with the new structure
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("node_monitoring", sa.Boolean(), nullable=False),
        sa.Column("node_auto_restart", sa.Boolean(), nullable=False),
    )  # pylint: disable=no-member


def downgrade() -> None:
    """Revert the settings table to its original structure."""
    # Drop the new settings table
    op.drop_table("settings")  # pylint: disable=no-member

    # Recreate the original settings table structure
    op.create_table(
        "settings",
        sa.Column("key", sa.VARCHAR(length=256), nullable=False),
        sa.Column("value", sa.VARCHAR(length=2048), nullable=True),
        sa.Column(
            "created_at",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DATETIME(), nullable=True),
    )  # pylint: disable=no-member
