"""add settings

Revision ID: ab1ce3ef2a57
Revises: 3e5deef43bf0
Create Date: 2024-10-13 01:42:55.733416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab1ce3ef2a57'
down_revision: Union[str, None] = '3e5deef43bf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create settings table
    op.create_table('settings',
        sa.Column('key', sa.String(256), primary_key=True),
        sa.Column('value', sa.String(2048), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

def downgrade():
    # Drop settings table
    op.drop_table('settings')