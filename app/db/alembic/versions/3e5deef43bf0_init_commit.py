# pylint: skip-file
"""init commit

Revision ID: 3e5deef43bf0
Revises:
Create Date: 2024-10-11 15:47:37.464534
"""
# pylint: disable=all

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = "3e5deef43bf0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the tokens table."""
    op.create_table(  # pylint: disable=no-member
        "tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )


def downgrade() -> None:
    """Drop the tokens table."""
    op.drop_table("tokens")  # pylint: disable=no-member
