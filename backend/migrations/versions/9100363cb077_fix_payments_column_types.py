"""Fix payments column types

Revision ID: 9100363cb077
Revises: 71a4bfdf4bf7
Create Date: 2025-08-25 12:40:11.997757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9100363cb077'
down_revision: Union[str, Sequence[str], None] = '71a4bfdf4bf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
