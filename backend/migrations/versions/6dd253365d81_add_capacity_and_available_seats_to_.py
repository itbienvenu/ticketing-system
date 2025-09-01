"""add capacity and available_seats to buses

Revision ID: 6dd253365d81
Revises: 122f26aaf95e
Create Date: 2025-09-01 22:34:00.413967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dd253365d81'
down_revision: Union[str, Sequence[str], None] = '122f26aaf95e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add with a default so SQLite can fill existing rows
    # op.add_column('buses', sa.Column('capacity', sa.Integer(), nullable=False, server_default="0"))
    # op.add_column('buses', sa.Column('available_seats', sa.Integer(), nullable=False, server_default="0"))

    # Optional: remove the server_default after migration if you don’t want it permanent
    # op.alter_column('buses', 'capacity', server_default=None)
    # op.alter_column('buses', 'available_seats', server_default=None)
    pass

def downgrade():
    pass
    # op.drop_column('buses', 'capacity')
    # op.drop_column('buses', 'available_seats')
