"""Category primary key update

Revision ID: 2eac4438dab1
Revises: b2d9ab03c188
Create Date: 2024-10-13 09:51:51.117685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2eac4438dab1'
down_revision: Union[str, None] = 'b2d9ab03c188'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('categories', 'id')
    op.add_column('categories', sa.Column('id', sa.Integer(), autoincrement=True))


def downgrade() -> None:
    op.drop_column('categories', 'id')