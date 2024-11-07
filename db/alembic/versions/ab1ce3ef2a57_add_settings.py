"""add settings

Revision ID: ab1ce3ef2a57
Revises: 3e5deef43bf0
Create Date: 2024-10-13 01:42:55.733416
"""
# pylint: disable=all

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = "ab1ce3ef2a57"
down_revision: Union[str, None] = "3e5deef43bf0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the settings table."""
    op.create_table(  # pylint: disable=no-member
        "settings",
        sa.Column("key", sa.String(256), primary_key=True),
        sa.Column("value", sa.String(2048), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.current_timestamp(),  # pylint: disable=not-callable
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Drop the settings table."""
    op.drop_table("settings")  # pylint: disable=no-member
